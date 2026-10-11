"""Loss functions with class imbalance mitigation."""

from typing import Dict, List
import torch
import torch.nn as nn


def compute_class_weights(class_counts: Dict[str, int], classes: List[str]) -> torch.Tensor:
    """Computes balanced inverse frequency class weights: N / (num_classes * n_c)."""
    total = sum(class_counts.values())
    num_classes = len(classes)
    weights = []
    for c in sorted(classes):
        cnt = class_counts.get(c, 0)
        w = total / (num_classes * max(cnt, 1))
        weights.append(w)
    return torch.tensor(weights, dtype=torch.float32)


def get_loss_criterion(
    class_counts: Dict[str, int], classes: List[str], weighted: bool = True, device: str = "cpu"
) -> nn.CrossEntropyLoss:
    if weighted and class_counts:
        weights = compute_class_weights(class_counts, classes).to(device)
        return nn.CrossEntropyLoss(weight=weights)
    return nn.CrossEntropyLoss()
