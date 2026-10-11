"""Validate image integrity, resolutions, and formats for agricultural datasets."""

import argparse
import json
import shutil
import sys
from pathlib import Path

from agriguard.datasets.validator import ImageValidator
from agriguard.utils.logger import get_logger

logger = get_logger("validate_images")


def validate_dataset(
    input_dir: str = "data/raw",
    corrupt_dir: str = "data/interim/corrupt",
    crop: str = "all",
) -> dict:
    in_path = Path(input_dir)
    corrupt_path = Path(corrupt_dir)
    corrupt_path.mkdir(parents=True, exist_ok=True)

    validator = ImageValidator(min_width=64, min_height=64, max_dimension=4096)

    crop_dirs = [p for p in in_path.iterdir() if p.is_dir()] if crop == "all" else [in_path / crop]

    summary = {
        "total_scanned": 0,
        "valid_count": 0,
        "corrupt_count": 0,
        "details_by_crop": {},
    }

    for c_dir in crop_dirs:
        if not c_dir.exists():
            continue
        c_name = c_dir.name
        logger.info(f"Scanning images for crop: {c_name}")
        c_valid = 0
        c_corrupt = 0
        errors = []

        for img_file in c_dir.rglob("*"):
            if not img_file.is_file():
                continue
            if img_file.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue

            summary["total_scanned"] += 1
            res = validator.validate_file(img_file)

            if res.is_valid:
                c_valid += 1
                summary["valid_count"] += 1
            else:
                c_corrupt += 1
                summary["corrupt_count"] += 1
                rel_path = img_file.relative_to(in_path)
                logger.warning(f"Corrupt or invalid image: {rel_path} - Reason: {res.error_message}")
                errors.append({"file": str(rel_path), "reason": res.error_message})

                # Quarantine corrupt image
                target_quarantine = corrupt_path / rel_path
                target_quarantine.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(img_file), str(target_quarantine))

        summary["details_by_crop"][c_name] = {
            "valid": c_valid,
            "corrupt": c_corrupt,
            "errors": errors,
        }

    logger.info(
        f"Validation complete. Total Scanned: {summary['total_scanned']}, "
        f"Valid: {summary['valid_count']}, Corrupted/Quarantined: {summary['corrupt_count']}"
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description="Validate agricultural dataset images")
    parser.add_argument("--input", default="data/raw", help="Input directory")
    parser.add_argument("--corrupt-dir", default="data/interim/corrupt", help="Quarantine directory")
    parser.add_argument("--crop", default="all", help="Specific crop or all")
    args = parser.parse_args()

    validate_dataset(args.input, args.corrupt_dir, args.crop)


if __name__ == "__main__":
    main()
