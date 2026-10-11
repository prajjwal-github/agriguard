"""Master dataset preparation pipeline orchestrator for AgriGuard AI."""

import argparse
import sys
from pathlib import Path

from agriguard.config.settings import load_yaml
from agriguard.utils.logger import get_logger
from scripts.audit_dataset import audit_dataset
from scripts.deduplicate_images import deduplicate_dataset
from scripts.discover_datasets import discover_datasets
from scripts.download_datasets import download_crop_dataset, CROP_SOURCE_MAPPING
from scripts.generate_manifest import build_manifest
from scripts.normalize_labels import normalize_labels
from scripts.split_dataset import split_dataset
from scripts.validate_images import validate_dataset

logger = get_logger("run_pipeline")


def run_pipeline(
    config_path: str = "configs/dataset.yaml",
    crops: list[str] | None = None,
    samples_per_class: int = 35,
    dry_run: bool = False,
):
    logger.info("=" * 60)
    logger.info("STARTING AGRIGUARD AI DATASET PIPELINE")
    logger.info("=" * 60)

    cfg = load_yaml(config_path) if Path(config_path).exists() else {}
    raw_dir = cfg.get("raw_data_dir", "data/raw")
    manifests_dir = cfg.get("manifests_dir", "data/manifests")
    reports_dir = cfg.get("reports_dir", "data/reports")
    seed = cfg.get("random_seed", 42)

    # 1. Discover
    logger.info("\n--- STAGE 1: Dataset Discovery ---")
    discover_datasets(output_path=f"{reports_dir}/discovery_report.json")

    # 2. Download
    logger.info("\n--- STAGE 2: Dataset Acquisition ---")
    target_crops = crops or ["rice_leaf", "apple_leaf", "grape_leaf", "tomato_leaf", "potato_leaf", "maize_leaf"]
    for c in target_crops:
        if c in CROP_SOURCE_MAPPING:
            download_crop_dataset(
                crop=c,
                output_base=raw_dir,
                samples_per_class=samples_per_class,
                dry_run=dry_run,
            )

    if dry_run:
        logger.info("\n[DRY RUN COMPLETE] No further modifications executed.")
        return

    # 3. Validate Images
    logger.info("\n--- STAGE 3: Image Validation & Quarantine ---")
    validate_dataset(input_dir=raw_dir, corrupt_dir="data/interim/corrupt")

    # 4. Normalize Labels
    logger.info("\n--- STAGE 4: Label Normalization ---")
    normalize_labels(base_dir=raw_dir)

    # 5. Deduplicate Images
    logger.info("\n--- STAGE 5: Perceptual Deduplication ---")
    deduplicate_dataset(input_dir=raw_dir, report_output=f"{reports_dir}/duplicate_report.json")

    # 6. Generate Master Manifest
    logger.info("\n--- STAGE 6: Master Manifest Generation ---")
    build_manifest(raw_dir=raw_dir, manifests_dir=manifests_dir)

    # 7. Leakage-Resistant Splitting
    logger.info("\n--- STAGE 7: Leakage-Resistant Dataset Splitting ---")
    split_dataset(manifests_dir=manifests_dir, seed=seed)

    # 8. Audit & Readiness Gates
    logger.info("\n--- STAGE 8: Dataset Audit & Quality Gate Verification ---")
    audit_dataset(manifests_dir=manifests_dir, reports_dir=reports_dir)

    logger.info("\n" + "=" * 60)
    logger.info("AGRIGUARD AI DATASET PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Run complete AgriGuard dataset pipeline")
    parser.add_argument("--config", default="configs/dataset.yaml", help="Dataset configuration path")
    parser.add_argument("--crop", default=None, help="Specific crop to process (default: all configured)")
    parser.add_argument("--samples-per-class", type=int, default=35, help="Number of authentic images per class")
    parser.add_argument("--dry-run", action="store_true", help="Simulate pipeline without modifying disk")
    args = parser.parse_args()

    crops = [args.crop] if args.crop else None
    run_pipeline(
        config_path=args.config,
        crops=crops,
        samples_per_class=args.samples_per_class,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
