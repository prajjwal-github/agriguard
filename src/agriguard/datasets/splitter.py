"""Leakage-resistant train/validation/test splitting for agricultural datasets."""

import random
from collections import defaultdict
from typing import Dict, List, Tuple


class LeakageResistantSplitter:
    def __init__(
        self,
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: int = 42,
    ):
        if not abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5:
            raise ValueError("Split ratios must sum exactly to 1.0")
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

    def split(
        self, records: List[Dict], cluster_map: Dict[str, str]
    ) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Splits records into train, val, and test while ensuring all items in a
        cluster (near-duplicates, source sequences) remain strictly in the same split.
        """
        rng = random.Random(self.seed)

        # Group records by condition and cluster
        class_clusters: Dict[str, Dict[str, List[Dict]]] = defaultdict(lambda: defaultdict(list))
        for rec in records:
            cond = rec.get("condition", "unknown")
            img_id = rec.get("image_id", "")
            cluster_id = cluster_map.get(img_id, img_id)
            class_clusters[cond][cluster_id].append(rec)

        train_records = []
        val_records = []
        test_records = []

        for cond, clusters in class_clusters.items():
            # Sort clusters descending by size so largest groups are absorbed by train (70% capacity)
            # preventing small splits (val/test at 15%) from being starved
            cluster_list = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

            # Calculate target counts of images for this class
            total_images = sum(len(items) for _, items in cluster_list)
            target_train = int(total_images * self.train_ratio)
            target_val = int(total_images * self.val_ratio)

            curr_train_count = 0
            curr_val_count = 0

            for cluster_id, items in cluster_list:
                if curr_train_count + len(items) <= target_train or (
                    curr_train_count == 0 and target_train > 0
                ):
                    for item in items:
                        item_copy = dict(item)
                        item_copy["split"] = "train"
                        train_records.append(item_copy)
                    curr_train_count += len(items)
                elif curr_val_count + len(items) <= target_val or (
                    curr_val_count == 0 and target_val > 0
                ):
                    for item in items:
                        item_copy = dict(item)
                        item_copy["split"] = "val"
                        val_records.append(item_copy)
                    curr_val_count += len(items)
                else:
                    for item in items:
                        item_copy = dict(item)
                        item_copy["split"] = "test"
                        test_records.append(item_copy)

        return train_records, val_records, test_records

    @staticmethod
    def verify_no_leakage(
        train: List[Dict], val: List[Dict], test: List[Dict], cluster_map: Dict[str, str]
    ) -> Tuple[bool, List[str]]:
        """Validates that no image ID or cluster appears in more than one split."""
        violations = []
        train_ids = {r["image_id"] for r in train}
        val_ids = {r["image_id"] for r in val}
        test_ids = {r["image_id"] for r in test}

        # Check direct ID leakage
        if t_v := train_ids.intersection(val_ids):
            violations.append(f"Image ID leakage between Train and Val: {len(t_v)} items")
        if t_te := train_ids.intersection(test_ids):
            violations.append(f"Image ID leakage between Train and Test: {len(t_te)} items")
        if v_te := val_ids.intersection(test_ids):
            violations.append(f"Image ID leakage between Val and Test: {len(v_te)} items")

        # Check cluster / near-duplicate leakage
        train_clusters = {cluster_map.get(r["image_id"], r["image_id"]) for r in train}
        val_clusters = {cluster_map.get(r["image_id"], r["image_id"]) for r in val}
        test_clusters = {cluster_map.get(r["image_id"], r["image_id"]) for r in test}

        if c_tv := train_clusters.intersection(val_clusters):
            violations.append(f"Cluster/Near-duplicate leakage between Train and Val: {len(c_tv)} clusters")
        if c_tt := train_clusters.intersection(test_clusters):
            violations.append(f"Cluster/Near-duplicate leakage between Train and Test: {len(c_tt)} clusters")
        if c_vt := val_clusters.intersection(test_clusters):
            violations.append(f"Cluster/Near-duplicate leakage between Val and Test: {len(c_vt)} clusters")

        return len(violations) == 0, violations
