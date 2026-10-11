"""Train crop-specific disease classification model."""

import argparse
import sys
from pathlib import Path
import torch
from torch.utils.data import DataLoader

from agriguard.config.settings import load_yaml
from agriguard.datasets.registry import DatasetRegistry
from agriguard.datasets.torch_dataset import AgriGuardDataset
from agriguard.preprocessing.transforms import get_eval_transforms, get_train_transforms
from agriguard.training.loss import get_loss_criterion
from agriguard.training.model_factory import create_model
from agriguard.training.trainer import ModelTrainer
from agriguard.utils.logger import get_logger

logger = get_logger("train_model")


def train_crop_model(
    crop: str,
    arch: str = "mobilenet_v3_small",
    epochs: int = 8,
    batch_size: int = 16,
    lr: float = 0.0005,
    device: str = "cpu",
    pretrained: bool = True,
    manifests_dir: str = "data/manifests",
    checkpoint_dir: str = "models/checkpoints",
    exported_dir: str = "models/exported",
):
    logger.info(f"=== INITIALIZING MODEL TRAINING FOR CROP: {crop} ({arch}) ===")

    registry = DatasetRegistry(manifests_dir)
    train_records = registry.get_records_by_split(crop, "train")
    val_records = registry.get_records_by_split(crop, "val")

    if not train_records:
        logger.error(f"No train split records found for crop '{crop}' in {manifests_dir}. Check manifest.")
        sys.exit(1)

    classes = sorted(list({r["condition"] for r in train_records + val_records}))
    logger.info(f"Detected {len(classes)} classes for {crop}: {classes}")
    category = train_records[0].get("category", "fruit_leaf")

    train_ds = AgriGuardDataset(
        records=train_records,
        classes=classes,
        transform=get_train_transforms((224, 224)),
    )
    val_ds = AgriGuardDataset(
        records=val_records,
        classes=classes,
        transform=get_eval_transforms((224, 224)),
    )

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)

    # Class weighting
    class_counts = train_ds.get_class_counts()
    criterion = get_loss_criterion(class_counts, classes, weighted=True, device=device)

    # Model instantiation
    model = create_model(arch, num_classes=len(classes), pretrained=pretrained, dropout=0.2)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    trainer = ModelTrainer(
        model=model,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        epochs=epochs,
        early_stopping_patience=4,
        checkpoint_dir=checkpoint_dir,
        crop=crop,
        arch=arch,
        classes=classes,
    )

    fit_results = trainer.fit(train_loader, val_loader)

    # Export production inference bundle
    export_path = Path(exported_dir) / f"{crop}_{arch}.pt"
    trainer.export_production_bundle(
        export_path=export_path,
        best_checkpoint_path=fit_results["best_checkpoint"],
        category=category,
    )

    logger.info(f"Model training and export finished successfully for {crop}!")
    return fit_results


def main():
    parser = argparse.ArgumentParser(description="Train crop disease classification model")
    parser.add_argument("--config", default="configs/training.yaml", help="Training config path")
    parser.add_argument("--crop", default="rice_leaf", help="Target crop identifier")
    parser.add_argument("--arch", default="mobilenet_v3_small", help="Neural network architecture")
    parser.add_argument("--epochs", type=int, default=8, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Training batch size")
    parser.add_argument("--lr", type=float, default=0.0005, help="Learning rate")
    parser.add_argument("--device", default="cpu", help="Compute device (cpu/cuda)")
    parser.add_argument("--no-pretrained", action="store_true", help="Train from scratch without pretrained weights")
    args = parser.parse_args()

    train_crop_model(
        crop=args.crop,
        arch=args.arch,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
        pretrained=not args.no_pretrained,
    )


if __name__ == "__main__":
    main()
