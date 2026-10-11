"""Detect exact and perceptual near-duplicate images across dataset splits."""

import argparse
import json
import sys
from pathlib import Path
from PIL import Image

from agriguard.datasets.deduplicator import DatasetDeduplicator, compute_dhash, compute_md5
from agriguard.utils.logger import get_logger

logger = get_logger("deduplicate_images")


def deduplicate_dataset(
    input_dir: str = "data/raw",
    report_output: str = "data/reports/duplicate_report.json",
    hamming_threshold: int = 4,
):
    base_path = Path(input_dir)
    records = []

    logger.info("Extracting perceptual and cryptographic hashes for all images...")
    for img_file in base_path.rglob("*"):
        if not img_file.is_file():
            continue
        if img_file.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue

        try:
            md5_val = compute_md5(img_file)
            phash_val = compute_dhash(img_file)
            with Image.open(img_file) as im:
                w, h = im.size

            parts = img_file.relative_to(base_path).parts
            crop = parts[0] if len(parts) > 1 else "unknown"
            condition = parts[1] if len(parts) > 2 else "unknown"

            records.append({
                "image_id": img_file.stem,
                "file_path": str(img_file.as_posix()),
                "crop": crop,
                "condition": condition,
                "width": w,
                "height": h,
                "md5": md5_val,
                "phash": phash_val,
            })
        except Exception as e:
            logger.warning(f"Error computing hash for {img_file}: {e}")

    logger.info(f"Computed hashes for {len(records)} images. Running cluster deduplication...")
    deduper = DatasetDeduplicator(hamming_threshold=hamming_threshold)
    unique, duplicates, cluster_map = deduper.find_duplicates(records)

    logger.info(f"Deduplication complete: {len(unique)} unique, {len(duplicates)} duplicates detected.")

    report = {
        "total_scanned": len(records),
        "unique_count": len(unique),
        "duplicate_count": len(duplicates),
        "hamming_threshold": hamming_threshold,
        "duplicates": duplicates,
    }

    out_file = Path(report_output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Duplicate report saved to {out_file}")
    return unique, duplicates, cluster_map


def main():
    parser = argparse.ArgumentParser(description="Find duplicate and near-duplicate images")
    parser.add_argument("--input", default="data/raw", help="Directory with raw images")
    parser.add_argument("--output", default="data/reports/duplicate_report.json", help="Report path")
    parser.add_argument("--threshold", type=int, default=4, help="Hamming distance threshold")
    args = parser.parse_args()

    deduplicate_dataset(args.input, args.output, args.threshold)


if __name__ == "__main__":
    main()
