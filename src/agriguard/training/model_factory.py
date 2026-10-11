"""Model factory for initializing vision classification architectures."""

from typing import List, Optional
import torch
import torch.nn as nn
import torchvision.models as models

SUPPORTED_ARCHITECTURES = [
    "mobilenet_v3_small",
    "mobilenet_v3_large",
    "resnet18",
    "efficientnet_b0",
]


def create_model(
    architecture: str,
    num_classes: int,
    pretrained: bool = False,
    dropout: float = 0.2,
) -> nn.Module:
    """Instantiates a neural network backbone with tailored classification head."""
    arch = architecture.lower()

    if arch == "mobilenet_v3_small":
        weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_small(weights=weights)
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    elif arch == "mobilenet_v3_large":
        weights = models.MobileNet_V3_Large_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_large(weights=weights)
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    elif arch == "resnet18":
        weights = models.ResNet18_Weights.DEFAULT if pretrained else None
        model = models.resnet18(weights=weights)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    elif arch == "efficientnet_b0":
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = models.efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    else:
        raise ValueError(
            f"Unsupported architecture '{architecture}'. Supported: {SUPPORTED_ARCHITECTURES}"
        )
