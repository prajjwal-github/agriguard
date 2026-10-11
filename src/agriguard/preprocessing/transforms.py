"""Image transforms and data augmentation for training and inference."""

from typing import Tuple
import torchvision.transforms as T


def get_train_transforms(image_size: Tuple[int, int] = (224, 224)) -> T.Compose:
    """Returns training transforms with mild, diagnostic-safe augmentations."""
    return T.Compose([
        T.Resize(image_size),
        T.RandomHorizontalFlip(p=0.5),
        T.RandomVerticalFlip(p=0.2),
        T.RandomRotation(degrees=15),
        T.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.1),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


def get_eval_transforms(image_size: Tuple[int, int] = (224, 224)) -> T.Compose:
    """Returns deterministic evaluation transforms without data distortion."""
    return T.Compose([
        T.Resize(image_size),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
