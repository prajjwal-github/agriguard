"""Generate master dataset manifest with provenance and verification metadata."""

import argparse
from pathlib import Path
from PIL import Image

from agriguard.datasets.deduplicator import DatasetDeduplicator, compute_dhash, compute_md5
from agriguard.datasets.registry import DatasetRegistry
from agriguard.datasets.validator import ImageValidator
from agriguard.utils.logger import get_logger

logger = get_logger("generate_manifest")

CROP_CATEGORY_MAP = {
    "apple": "fruit",
    "banana": "fruit",
    "orange": "fruit",
    "apple_leaf": "fruit_leaf",
    "grape_leaf": "fruit_leaf",
    "tomato_leaf": "vegetable_leaf",
    "potato_leaf": "vegetable_leaf",
    "rice_leaf": "grain_crop_leaf",
    "maize_leaf": "grain_crop_leaf",
    "chilli_leaf": "vegetable_leaf",
}

CROP_LICENSE_MAP = {
    "apple": "Apache License 2.0 / Fruit Freshness Dataset (Chen et al.)",
    "banana": "Apache License 2.0 / Fruit Freshness Dataset (Chen et al.)",
    "orange": "Apache License 2.0 / Fruit Freshness Dataset (Chen et al.)",
    "rice_leaf": "CC BY 4.0 / Prajapati et al. (Computers and Electronics in Agriculture 2017)",
    "apple_leaf": "CC BY 4.0 / Hughes & Salathé (Penn State University)",
    "grape_leaf": "CC BY 4.0 / Hughes & Salathé (Penn State University)",
    "tomato_leaf": "CC BY 4.0 / Hughes & Salathé (Penn State University)",
    "potato_leaf": "CC BY 4.0 / Hughes & Salathé (Penn State University)",
    "maize_leaf": "CC BY 4.0 / Hughes & Salathé (Penn State University)",
    "chilli_leaf": "CC BY 4.0 / Hughes & Salathé (Penn State University)",
}


def build_manifest(raw_dir: str = "data/raw", manifests_dir: str = "data/manifests") -> list:
    raw_path = Path(raw_dir)
    validator = ImageValidator()
    records = []

    logger.info(f"Scanning raw images in {raw_dir} to construct master manifest...")
    for img_path in sorted(raw_path.rglob("*")):
        if not img_path.is_file():
            continue
        if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue

        parts = img_path.relative_to(raw_path).parts
        if len(parts) < 2:
            continue
        crop = parts[0]
        condition = parts[1]

        v_res = validator.validate_file(img_path)
        if not v_res.is_valid:
            continue

        md5 = compute_md5(img_path)
        phash = compute_dhash(img_path)

        rec = {
            "image_id": f"{crop}_{condition}_{img_path.stem}",
            "file_path": str(img_path.as_posix()),
            "category": CROP_CATEGORY_MAP.get(crop, "unknown"),
            "crop": crop,
            "plant_part": "fruit_surface" if crop in ["apple", "banana", "orange"] else "leaf",
            "condition": condition,
            "source_dataset": (
                "Fruit Freshness Detection Benchmark (Chen et al.)"
                if crop in ["apple", "banana", "orange"]
                else ("Rice Leaf Disease Benchmark (Prajapati et al.)" if crop == "rice_leaf" else "PlantVillage Open Research Dataset")
            ),
            "license": CROP_LICENSE_MAP.get(crop, "CC BY 4.0"),
            "md5": md5,
            "phash": phash,
            "width": v_res.width,
            "height": v_res.height,
            "format": v_res.format,
            "label_status": "verified",
            "split": "unassigned",
        }
        records.append(rec)

    # Compute cluster IDs using deduplicator
    deduper = DatasetDeduplicator(hamming_threshold=4)
    _, _, cluster_map = deduper.find_duplicates(records)
    for rec in records:
        rec["cluster_id"] = cluster_map.get(rec["image_id"], rec["image_id"])

    registry = DatasetRegistry(manifests_dir)
    registry.save_manifest(records)
    logger.info(f"Master manifest generated with {len(records)} verified images.")
    return records


def main():
    parser = argparse.ArgumentParser(description="Generate master dataset manifest")
    parser.add_argument("--raw-dir", default="data/raw", help="Raw images directory")
    parser.add_argument("--manifests-dir", default="data/manifests", help="Manifest output directory")
    args = parser.parse_args()

    build_manifest(args.raw_dir, args.manifests_dir)


if __name__ == "__main__":
    main()
