"""PyTorch Dataset loader backed by the AgriGuard Master Manifest."""

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from PIL import Image, ImageOps
import torch
from torch.utils.data import Dataset


class AgriGuardDataset(Dataset):
    def __init__(
        self,
        records: List[Dict],
        classes: List[str],
        transform: Optional[Callable] = None,
    ):
        self.records = records
        self.classes = sorted(classes)
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}
        self.idx_to_class = {i: c for i, c in enumerate(self.classes)}
        self.transform = transform

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        rec = self.records[idx]
        file_path = Path(rec["file_path"])
        cond = rec["condition"]

        if not file_path.exists():
            raise FileNotFoundError(f"Image file missing from manifest path: {file_path}")

        with Image.open(file_path) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGB")

        if self.transform:
            img_tensor = self.transform(img)
        else:
            import torchvision.transforms.functional as TF
            img_tensor = TF.to_tensor(img)

        target = self.class_to_idx[cond]
        return img_tensor, target

    def get_class_counts(self) -> Dict[str, int]:
        counts = {c: 0 for c in self.classes}
        for r in self.records:
            cond = r["condition"]
            if cond in counts:
                counts[cond] += 1
        return counts
