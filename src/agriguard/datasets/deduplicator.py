"""Perceptual and cryptographic deduplication for agricultural datasets."""

import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from PIL import Image


def compute_md5(file_path: str | Path) -> str:
    """Calculates cryptographic MD5 checksum of a file."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_dhash(file_path: str | Path, hash_size: int = 8) -> str:
    """Computes difference hash (dHash) for perceptual similarity comparison."""
    with Image.open(file_path) as img:
        img = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())

    diff = []
    width = hash_size + 1
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * width + col]
            right = pixels[row * width + col + 1]
            diff.append(1 if left > right else 0)

    # Convert binary list to hex string
    decimal_val = 0
    for bit in diff:
        decimal_val = (decimal_val << 1) | bit
    hex_len = (hash_size * hash_size) // 4
    return f"{decimal_val:0{hex_len}x}"


def hamming_distance(hex_hash1: str, hex_hash2: str) -> int:
    """Computes bitwise Hamming distance between two hex-encoded hashes."""
    if len(hex_hash1) != len(hex_hash2):
        raise ValueError("Hashes must be of equal length")
    val1 = int(hex_hash1, 16)
    val2 = int(hex_hash2, 16)
    xor_val = val1 ^ val2
    return bin(xor_val).count("1")


class DatasetDeduplicator:
    def __init__(self, hamming_threshold: int = 4):
        self.hamming_threshold = hamming_threshold

    def find_duplicates(
        self, records: List[Dict]
    ) -> Tuple[List[Dict], List[Dict], Dict[str, str]]:
        """
        Analyzes records for exact MD5 and perceptual dHash duplicates.
        Returns:
            unique_records: filtered list with duplicates flagged/removed
            duplicate_records: list of identified duplicates
            hash_cluster_map: mapping from image_id to cluster_id for leakage-proof splitting
        """
        seen_md5: Dict[str, str] = {}
        unique_records = []
        duplicate_records = []
        cluster_map: Dict[str, str] = {}

        # First pass: MD5 exact match
        non_md5_duplicates = []
        for rec in records:
            md5 = rec.get("md5")
            rec_id = rec.get("image_id")
            if md5 in seen_md5:
                rec_copy = dict(rec)
                rec_copy["duplicate_of"] = seen_md5[md5]
                rec_copy["duplicate_type"] = "exact_md5"
                duplicate_records.append(rec_copy)
                cluster_map[rec_id] = seen_md5[md5]
            else:
                seen_md5[md5] = rec_id
                cluster_map[rec_id] = rec_id
                non_md5_duplicates.append(rec)

        # Second pass: Perceptual dHash near-duplicates
        accepted_hashes: List[Tuple[str, str]] = []  # (hash, image_id)
        for rec in non_md5_duplicates:
            phash = rec.get("phash")
            rec_id = rec.get("image_id")
            is_near_dup = False
            matched_id = None

            if phash:
                for existing_hash, existing_id in accepted_hashes:
                    dist = hamming_distance(phash, existing_hash)
                    if dist <= self.hamming_threshold:
                        is_near_dup = True
                        matched_id = existing_id
                        break

            if is_near_dup and matched_id:
                rec_copy = dict(rec)
                rec_copy["duplicate_of"] = matched_id
                rec_copy["duplicate_type"] = "perceptual_dhash"
                duplicate_records.append(rec_copy)
                cluster_map[rec_id] = matched_id
            else:
                unique_records.append(rec)
                if phash:
                    accepted_hashes.append((phash, rec_id))

        return unique_records, duplicate_records, cluster_map
