"""Dataset download engine for authentic agricultural datasets with concurrent downloads."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
import requests

from agriguard.utils.logger import get_logger

logger = get_logger("download_datasets")

CROP_SOURCE_MAPPING = {
    "rice_leaf": {
        "repo": "MHassaanButt/Rice-Disease-Classfication",
        "subpath": "Dataset",
        "classes": {
            "bacterial_leaf_blight": "Bacterial leaf blight",
            "brown_spot": "Brown spot",
            "leaf_smut": "Leaf smut",
        },
        "license": "CC BY 4.0 / Prajapati et al.",
        "category": "grain_crop_leaf",
    },
    "apple_leaf": {
        "repo": "spMohanty/PlantVillage-Dataset",
        "subpath": "raw/color",
        "classes": {
            "apple_scab": "Apple___Apple_scab",
            "black_rot": "Apple___Black_rot",
            "cedar_apple_rust": "Apple___Cedar_apple_rust",
            "healthy": "Apple___healthy",
        },
        "license": "CC BY 4.0 / Hughes & Salathé (Penn State)",
        "category": "fruit_leaf",
    },
    "grape_leaf": {
        "repo": "spMohanty/PlantVillage-Dataset",
        "subpath": "raw/color",
        "classes": {
            "black_rot": "Grape___Black_rot",
            "esca_black_measles": "Grape___Esca_(Black_Measles)",
            "leaf_blight": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "healthy": "Grape___healthy",
        },
        "license": "CC BY 4.0 / Hughes & Salathé (Penn State)",
        "category": "fruit_leaf",
    },
    "tomato_leaf": {
        "repo": "spMohanty/PlantVillage-Dataset",
        "subpath": "raw/color",
        "classes": {
            "bacterial_spot": "Tomato___Bacterial_spot",
            "early_blight": "Tomato___Early_blight",
            "late_blight": "Tomato___Late_blight",
            "septoria_leaf_spot": "Tomato___Septoria_leaf_spot",
            "healthy": "Tomato___healthy",
        },
        "license": "CC BY 4.0 / Hughes & Salathé (Penn State)",
        "category": "vegetable_leaf",
    },
    "potato_leaf": {
        "repo": "spMohanty/PlantVillage-Dataset",
        "subpath": "raw/color",
        "classes": {
            "early_blight": "Potato___Early_blight",
            "late_blight": "Potato___Late_blight",
            "healthy": "Potato___healthy",
        },
        "license": "CC BY 4.0 / Hughes & Salathé (Penn State)",
        "category": "vegetable_leaf",
    },
    "maize_leaf": {
        "repo": "spMohanty/PlantVillage-Dataset",
        "subpath": "raw/color",
        "classes": {
            "cercospora_leaf_spot": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "common_rust": "Corn_(maize)___Common_rust_",
            "northern_leaf_blight": "Corn_(maize)___Northern_Leaf_Blight",
            "healthy": "Corn_(maize)___healthy",
        },
        "license": "CC BY 4.0 / Hughes & Salathé (Penn State)",
        "category": "grain_crop_leaf",
    },
    "chilli_leaf": {
        "repo": "spMohanty/PlantVillage-Dataset",
        "subpath": "raw/color",
        "classes": {
            "bacterial_spot": "Pepper,_bell___Bacterial_spot",
            "healthy": "Pepper,_bell___healthy",
        },
        "license": "CC BY 4.0 / Hughes & Salathé (Penn State)",
        "category": "vegetable_leaf",
    },
}


def download_single_image(session: requests.Session, download_url: str, target_file: Path) -> bool:
    if target_file.exists() and target_file.stat().st_size > 0:
        return True

    for attempt in range(3):
        try:
            res = session.get(download_url, timeout=12)
            if res.status_code == 200 and len(res.content) > 1000:
                with open(target_file, "wb") as f:
                    f.write(res.content)
                return True
        except Exception:
            time.sleep(0.5)
    return False


def download_crop_dataset(
    crop: str,
    output_base: str = "data/raw",
    samples_per_class: int = 35,
    max_workers: int = 6,
    dry_run: bool = False,
) -> int:
    if crop not in CROP_SOURCE_MAPPING:
        logger.error(f"Crop '{crop}' is not configured for automated download.")
        return 0

    meta = CROP_SOURCE_MAPPING[crop]
    repo = meta["repo"]
    subpath = meta["subpath"]
    classes = meta["classes"]
    out_dir = Path(output_base) / crop
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Initiating concurrent download for crop: {crop} ({meta['category']}) from {repo}")
    total_available = 0

    session = requests.Session()
    session.headers.update({"User-Agent": "AgriGuard-Downloader-v1.0"})

    for canonical_class, remote_folder in classes.items():
        class_dir = out_dir / canonical_class
        class_dir.mkdir(parents=True, exist_ok=True)

        existing_files = [
            f for f in class_dir.iterdir()
            if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"] and f.stat().st_size > 0
        ]
        if len(existing_files) >= samples_per_class:
            logger.info(f"Class '{canonical_class}' already has {len(existing_files)} images locally.")
            total_available += len(existing_files)
            continue

        api_url = f"https://api.github.com/repos/{repo}/contents/{subpath}/{remote_folder}"
        try:
            res = session.get(api_url, timeout=15)
            if res.status_code != 200:
                logger.warning(f"Could not list remote folder {remote_folder} (HTTP {res.status_code})")
                continue

            items = res.json()
            if not isinstance(items, list):
                continue

            image_items = [
                it for it in items
                if it.get("name", "").lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ][:samples_per_class]

            logger.info(f"Downloading up to {len(image_items)} images for {crop}/{canonical_class}...")
            if dry_run:
                total_available += len(image_items)
                continue

            download_tasks = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for item in image_items:
                    target_file = class_dir / item["name"]
                    dl_url = item.get("download_url")
                    if dl_url:
                        download_tasks.append(
                            executor.submit(download_single_image, session, dl_url, target_file)
                        )

                class_success = sum(1 for fut in as_completed(download_tasks) if fut.result())
                total_available += class_success
                logger.info(f"  --> Successfully obtained {class_success} images for {canonical_class}.")

        except Exception as e:
            logger.error(f"Error accessing GitHub for {canonical_class}: {e}")

    logger.info(f"Completed download stage for {crop}. Total images available: {total_available}")
    return total_available


def main():
    parser = argparse.ArgumentParser(description="Download authentic agricultural datasets concurrently")
    parser.add_argument("--crop", default="rice_leaf", choices=list(CROP_SOURCE_MAPPING.keys()) + ["all"], help="Crop to download")
    parser.add_argument("--output", default="data/raw", help="Output base directory")
    parser.add_argument("--samples-per-class", type=int, default=35, help="Max authentic samples per class")
    parser.add_argument("--max-workers", type=int, default=6, help="Thread pool workers")
    parser.add_argument("--dry-run", action="store_true", help="Simulate download without saving files")
    args = parser.parse_args()

    if args.crop == "all":
        for c in CROP_SOURCE_MAPPING.keys():
            download_crop_dataset(c, args.output, args.samples_per_class, args.max_workers, args.dry_run)
    else:
        download_crop_dataset(args.crop, args.output, args.samples_per_class, args.max_workers, args.dry_run)


if __name__ == "__main__":
    main()
