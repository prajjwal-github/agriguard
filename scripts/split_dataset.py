"""Create leakage-resistant train (70%), validation (15%), and test (15%) splits."""

import argparse
from pathlib import Path
from collections import defaultdict

from agriguard.datasets.registry import DatasetRegistry
from agriguard.datasets.splitter import LeakageResistantSplitter
from agriguard.utils.logger import get_logger

logger = get_logger("split_dataset")


def split_dataset(manifests_dir: str = "data/manifests", seed: int = 42):
    registry = DatasetRegistry(manifests_dir)
    records = registry.load_manifest()

    if not records:
        logger.error("No records found in master manifest. Run generate_manifest first.")
        return

    logger.info(f"Loaded {len(records)} records from manifest. Partitioning by crop...")
    crop_records = defaultdict(list)
    for r in records:
        crop_records[r["crop"]].append(r)

    splitter = LeakageResistantSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=seed)
    updated_records = []

    for crop, c_records in crop_records.items():
        cluster_map = {r["image_id"]: r.get("cluster_id", r["image_id"]) for r in c_records}
        train, val, test = splitter.split(c_records, cluster_map)

        # Leakage verification
        no_leakage, violations = splitter.verify_no_leakage(train, val, test, cluster_map)
        if not no_leakage:
            logger.error(f"Leakage detected in crop {crop}: {violations}")
            raise RuntimeError(f"Data leakage detected for {crop}")

        logger.info(
            f"Split for '{crop}': Train={len(train)} ({len(train)/len(c_records)*100:.1f}%), "
            f"Val={len(val)} ({len(val)/len(c_records)*100:.1f}%), "
            f"Test={len(test)} ({len(test)/len(c_records)*100:.1f}%) | Leakage: ZERO"
        )
        updated_records.extend(train + val + test)

    registry.save_manifest(updated_records)
    logger.info("Updated master manifest with verified split assignments.")


def main():
    parser = argparse.ArgumentParser(description="Assign train/val/test splits")
    parser.add_argument("--manifests-dir", default="data/manifests", help="Manifests directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    split_dataset(args.manifests_dir, args.seed)


if __name__ == "__main__":
    main()
