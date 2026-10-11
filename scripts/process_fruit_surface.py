"""Extract and organize authentic Fruit Surface dataset from cloned repository."""

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
from agriguard.utils.logger import get_logger

logger = get_logger("process_fruit_surface")

FRUIT_CLASS_MAPPING = {
    "fresh_apple": ("apple", "healthy"),
    "normal_apple": ("apple", "minor_blemish"),
    "rotten_apple": ("apple", "rot_decay"),
    "fresh_banana": ("banana", "healthy"),
    "normal_banana": ("banana", "minor_blemish"),
    "rotten_banana": ("banana", "rot_decay"),
    "fresh_orange": ("orange", "healthy"),
    "normal_orange": ("orange", "minor_blemish"),
    "rotten_orange": ("orange", "rot_decay"),
}

def process_fruit_surface(
    raw_source_dir: str = "data/interim/fruit_surface_raw",
    output_base: str = "data/raw",
    max_samples_per_class: int = 60,
):
    src_dir = Path(raw_source_dir)
    annot_dir = src_dir / "Annotations"
    img_dir = src_dir / "JPEGImages"

    if not annot_dir.exists() or not img_dir.exists():
        logger.error(f"Source annotations or images not found in {src_dir}")
        return

    logger.info("Extracting and organizing Fruit Surface images...")
    class_counts = defaultdict(int)

    xml_files = sorted(list(annot_dir.glob("*.xml")))
    logger.info(f"Scanning {len(xml_files)} annotation files...")

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            filename_elem = root.find("filename")
            if filename_elem is None:
                continue
            img_filename = filename_elem.text
            src_img_path = img_dir / img_filename
            if not src_img_path.exists():
                continue

            objects = root.findall("object")
            if not objects:
                continue

            # Get primary object
            raw_class_name = objects[0].find("name").text
            if raw_class_name not in FRUIT_CLASS_MAPPING:
                continue

            crop_id, canonical_condition = FRUIT_CLASS_MAPPING[raw_class_name]
            key = f"{crop_id}/{canonical_condition}"

            if class_counts[key] >= max_samples_per_class:
                continue

            target_dir = Path(output_base) / crop_id / canonical_condition
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / img_filename

            if not target_path.exists():
                shutil.copy2(src_img_path, target_path)

            class_counts[key] += 1

        except Exception as e:
            continue

    logger.info("Fruit Surface extraction complete! Class counts:")
    for k, count in sorted(class_counts.items()):
        logger.info(f"  {k}: {count} images")

if __name__ == "__main__":
    process_fruit_surface()
