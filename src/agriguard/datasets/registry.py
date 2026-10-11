"""Dataset Registry and Manifest Management for AgriGuard AI."""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional


class DatasetRegistry:
    def __init__(self, manifests_dir: str | Path = "data/manifests"):
        self.manifests_dir = Path(manifests_dir)
        self.manifests_dir.mkdir(parents=True, exist_ok=True)
        self.master_manifest_json = self.manifests_dir / "master_manifest.json"
        self.master_manifest_csv = self.manifests_dir / "master_manifest.csv"

    def save_manifest(self, records: List[Dict]) -> None:
        """Saves records to both JSON and CSV master manifests."""
        # Save JSON
        with open(self.master_manifest_json, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        # Save CSV
        if records:
            fieldnames = list(records[0].keys())
            with open(self.master_manifest_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)

    def load_manifest(self) -> List[Dict]:
        """Loads records from the master JSON manifest."""
        if not self.master_manifest_json.exists():
            return []
        with open(self.master_manifest_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_records_by_crop(self, crop: str) -> List[Dict]:
        """Filters manifest records by crop identifier."""
        return [r for r in self.load_manifest() if r.get("crop") == crop]

    def get_records_by_split(self, crop: str, split: str) -> List[Dict]:
        """Filters records for a specific crop and split (train/val/test)."""
        return [
            r for r in self.load_manifest()
            if r.get("crop") == crop and r.get("split") == split
        ]
