"""Manual curation and field ingestion workflow for categories lacking public datasets."""

import argparse
import shutil
from pathlib import Path

from agriguard.datasets.validator import ImageValidator
from agriguard.utils.logger import get_logger

logger = get_logger("curate_manual_dataset")


def ingest_field_sample(
    image_file: str | Path,
    category: str,
    crop: str,
    condition: str,
    annotator_name: str,
    notes: str = "",
    target_base: str = "data/raw",
) -> bool:
    """Ingests a verified field sample with validator checks and audit logging."""
    src = Path(image_file)
    if not src.exists():
        logger.error(f"Source file {src} not found.")
        return False

    validator = ImageValidator()
    v_res = validator.validate_file(src)
    if not v_res.is_valid:
        logger.error(f"Image validation rejected: {v_res.error_message}")
        return False

    dest_dir = Path(target_base) / crop / condition
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / f"manual_{annotator_name}_{src.name}"

    shutil.copy2(src, dest_file)
    logger.info(
        f"Successfully ingested {src.name} -> {dest_file} "
        f"[Category: {category}, Crop: {crop}, Condition: {condition}, Annotator: {annotator_name}]"
    )
    return True


def main():
    parser = argparse.ArgumentParser(description="Ingest manually curated field observations")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--category", required=True, help="Category (fruit, fruit_leaf, vegetable, etc.)")
    parser.add_argument("--crop", required=True, help="Crop identifier (e.g. apple, tomato)")
    parser.add_argument("--condition", required=True, help="Condition or disease label")
    parser.add_argument("--annotator", default="field_agronomist", help="Reviewer or annotator ID")
    parser.add_argument("--notes", default="", help="Agronomic field notes")
    args = parser.parse_args()

    ingest_field_sample(
        image_file=args.image,
        category=args.category,
        crop=args.crop,
        condition=args.condition,
        annotator_name=args.annotator,
        notes=args.notes,
    )


if __name__ == "__main__":
    main()
