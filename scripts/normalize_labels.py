"""Normalize dataset directory structures and class labels against canonical taxonomy."""

import argparse
import sys
from pathlib import Path
import yaml

from agriguard.utils.logger import get_logger

logger = get_logger("normalize_labels")


def normalize_labels(
    base_dir: str = "data/raw",
    taxonomy_path: str = "datasets/taxonomy.yaml",
    dry_run: bool = False,
):
    base_path = Path(base_dir)
    tax_file = Path(taxonomy_path)

    if not tax_file.exists():
        logger.error(f"Taxonomy file not found: {tax_file}")
        sys.exit(1)

    with open(tax_file, "r", encoding="utf-8") as f:
        taxonomy = yaml.safe_load(f)

    normalized_map = taxonomy.get("normalized_conditions", {})

    logger.info("Scanning dataset folders for taxonomy normalization...")
    for crop_dir in base_path.iterdir():
        if not crop_dir.is_dir():
            continue
        crop_name = crop_dir.name
        expected_classes = normalized_map.get(crop_name, [])

        for class_dir in crop_dir.iterdir():
            if not class_dir.is_dir():
                continue
            curr_name = class_dir.name

            # Check if current name matches an expected canonical name
            canonical_match = None
            for exp in expected_classes:
                if curr_name.lower().replace(" ", "_").replace("-", "_") == exp:
                    canonical_match = exp
                    break

            if canonical_match and canonical_match != curr_name:
                target_dir = crop_dir / canonical_match
                logger.info(f"Renaming non-canonical label: {curr_name} -> {canonical_match}")
                if not dry_run:
                    class_dir.rename(target_dir)
            elif curr_name in expected_classes:
                logger.info(f"  Verified canonical class: {crop_name}/{curr_name}")
            else:
                logger.warning(f"  Non-standard class detected: {crop_name}/{curr_name} (Not in canonical taxonomy)")

    logger.info("Label normalization scan completed.")


def main():
    parser = argparse.ArgumentParser(description="Normalize dataset folder labels")
    parser.add_argument("--base-dir", default="data/raw", help="Base directory with raw images")
    parser.add_argument("--taxonomy", default="datasets/taxonomy.yaml", help="Taxonomy file path")
    parser.add_argument("--dry-run", action="store_true", help="Preview renames without executing")
    args = parser.parse_args()

    normalize_labels(args.base_dir, args.taxonomy, args.dry_run)


if __name__ == "__main__":
    main()
