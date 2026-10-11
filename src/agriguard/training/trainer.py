"""Model training engine with checkpointing and early stopping."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import torch
import torch.nn as nn
from sklearn.metrics import f1_score, accuracy_score

from agriguard.utils.logger import get_logger

logger = get_logger("trainer")


class ModelTrainer:
    def __init__(
        self,
        model: nn.Module,
        criterion: nn.Module,
        optimizer: torch.optim.Optimizer,
        scheduler: Optional[Any] = None,
        device: str = "cpu",
        epochs: int = 8,
        early_stopping_patience: int = 3,
        checkpoint_dir: str = "models/checkpoints",
        crop: str = "unknown",
        arch: str = "mobilenet_v3_small",
        classes: Optional[List[str]] = None,
    ):
        self.model = model.to(device)
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        self.epochs = epochs
        self.early_stopping_patience = early_stopping_patience
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.crop = crop
        self.arch = arch
        self.classes = classes or []
        self.history: List[Dict[str, Any]] = []

    def train_epoch(self, dataloader) -> Tuple[float, float]:
        self.model.train()
        running_loss = 0.0
        all_preds = []
        all_targets = []

        for images, targets in dataloader:
            images = images.to(self.device)
            targets = targets.to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * images.size(0)
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().tolist())
            all_targets.extend(targets.cpu().tolist())

        epoch_loss = running_loss / max(len(dataloader.dataset), 1)
        epoch_acc = accuracy_score(all_targets, all_preds)
        return epoch_loss, epoch_acc

    @torch.no_grad()
    def evaluate(self, dataloader) -> Tuple[float, float, float]:
        self.model.eval()
        running_loss = 0.0
        all_preds = []
        all_targets = []

        for images, targets in dataloader:
            images = images.to(self.device)
            targets = targets.to(self.device)

            outputs = self.model(images)
            loss = self.criterion(outputs, targets)

            running_loss += loss.item() * images.size(0)
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().tolist())
            all_targets.extend(targets.cpu().tolist())

        val_loss = running_loss / max(len(dataloader.dataset), 1)
        val_acc = accuracy_score(all_targets, all_preds)
        val_f1 = f1_score(all_targets, all_preds, average="macro", zero_division=0)
        return val_loss, val_acc, val_f1

    def fit(self, train_loader, val_loader) -> Dict[str, Any]:
        logger.info(f"Starting training for {self.crop} ({self.arch}) on {self.device} for {self.epochs} epochs.")
        best_val_f1 = -1.0
        patience_counter = 0
        best_checkpoint_path = self.checkpoint_dir / f"{self.crop}_{self.arch}_best.pt"

        for epoch in range(1, self.epochs + 1):
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc, val_f1 = self.evaluate(val_loader)

            if self.scheduler:
                self.scheduler.step()

            epoch_record = {
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "train_acc": round(train_acc, 4),
                "val_loss": round(val_loss, 4),
                "val_acc": round(val_acc, 4),
                "val_macro_f1": round(val_f1, 4),
            }
            self.history.append(epoch_record)

            logger.info(
                f"Epoch {epoch:02d}/{self.epochs:02d} | "
                f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.1f}% | "
                f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.1f}% Macro-F1: {val_f1:.4f}"
            )

            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                patience_counter = 0
                torch.save(
                    {
                        "epoch": epoch,
                        "model_state_dict": self.model.state_dict(),
                        "optimizer_state_dict": self.optimizer.state_dict(),
                        "best_val_f1": best_val_f1,
                        "crop": self.crop,
                        "architecture": self.arch,
                        "classes": self.classes,
                    },
                    best_checkpoint_path,
                )
                logger.info(f"  --> Saved new best checkpoint to {best_checkpoint_path} (F1: {best_val_f1:.4f})")
            else:
                patience_counter += 1
                if patience_counter >= self.early_stopping_patience:
                    logger.info(f"Early stopping triggered at epoch {epoch} (no improvement for {patience_counter} epochs).")
                    break

        return {
            "best_val_f1": best_val_f1,
            "best_checkpoint": str(best_checkpoint_path),
            "history": self.history,
        }

    def export_production_bundle(
        self,
        export_path: str | Path,
        best_checkpoint_path: Optional[str | Path] = None,
        category: str = "fruit_leaf",
    ) -> Path:
        """Exports standalone deployable model bundle for API inference."""
        target_path = Path(export_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        ckpt_file = Path(best_checkpoint_path) if best_checkpoint_path else self.checkpoint_dir / f"{self.crop}_{self.arch}_best.pt"
        if ckpt_file.exists():
            ckpt = torch.load(ckpt_file, map_location="cpu", weights_only=False)
            state_dict = ckpt["model_state_dict"]
        else:
            state_dict = self.model.state_dict()

        bundle = {
            "model_state_dict": state_dict,
            "architecture": self.arch,
            "crop": self.crop,
            "category": category,
            "classes": self.classes,
            "num_classes": len(self.classes),
            "input_resolution": [224, 224],
            "normalization": {
                "mean": [0.485, 0.456, 0.406],
                "std": [0.229, 0.224, 0.225],
            },
            "exported_at": datetime.now(timezone.utc).isoformat(),
        }
        torch.save(bundle, target_path)
        logger.info(f"Production model bundle exported to {target_path}")
        return target_path
