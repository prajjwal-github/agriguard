"""Model Registry and Hierarchical Routing Engine for AgriGuard AI."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import torch
import torch.nn as nn
import yaml

from agriguard.training.model_factory import create_model
from agriguard.utils.logger import get_logger

logger = get_logger("model_router")


@dataclass
class RoutedModel:
    model: nn.Module
    architecture: str
    crop: str
    category: str
    classes: List[str]
    input_resolution: list[int]
    gradcam_target_layer: nn.Module


class ModelRouter:
    def __init__(self, registry_config_path: str = "configs/models.yaml", device: str = "cpu"):
        self.config_path = Path(registry_config_path)
        self.device = device
        self.registry: Dict[str, Any] = {}
        self.model_cache: Dict[str, RoutedModel] = {}
        self.load_registry()

    def load_registry(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Model registry config missing: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.registry = yaml.safe_load(f) or {}
        logger.info(f"Model router loaded registry version {self.registry.get('registry_version')}")

    def get_categories(self) -> Dict[str, Any]:
        """Returns registered primary categories and metadata."""
        cats = self.registry.get("categories", {})
        result = {}
        for cat_id, meta in cats.items():
            result[cat_id] = {
                "category_id": cat_id,
                "display_name": meta.get("display_name"),
                "description": meta.get("description"),
                "supported_crops_count": len(meta.get("crops", {})),
            }
        return result

    def get_crops_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        """Returns all registered crops for a selected category with readiness status."""
        cats = self.registry.get("categories", {})
        if category_id not in cats:
            raise ValueError(f"Category '{category_id}' does not exist in registry.")

        crops = cats[category_id].get("crops", {})
        result = []
        for crop_id, meta in crops.items():
            active_model = meta.get("active_model")
            is_available = bool(active_model and Path(active_model).exists())
            status = "ready" if is_available else meta.get("status", "planned")

            result.append({
                "crop_id": crop_id,
                "display_name": meta.get("display_name"),
                "status": status,
                "is_available": is_available,
                "task": meta.get("task", "classification"),
                "classes": meta.get("classes", []),
            })
        return result

    def route_and_load(self, category: str, crop: str) -> RoutedModel:
        """
        Validates category/crop hierarchy and returns cached model instance.
        Throws ValueError or FileNotFoundError if unsupported or missing.
        """
        cache_key = f"{category}_{crop}"
        if cache_key in self.model_cache:
            return self.model_cache[cache_key]

        cats = self.registry.get("categories", {})
        if category not in cats:
            raise ValueError(f"Unknown category '{category}'. Available: {list(cats.keys())}")

        crops = cats[category].get("crops", {})
        if crop not in crops:
            raise ValueError(
                f"Crop '{crop}' is not registered under category '{category}'. "
                f"Available in this category: {list(crops.keys())}"
            )

        crop_meta = crops[crop]
        status = crop_meta.get("status")
        model_rel_path = crop_meta.get("active_model")

        if not model_rel_path or status == "planned":
            raise ValueError(
                f"Model for crop '{crop}' in category '{category}' is currently in active development. "
                "AgriGuard AI does not fabricate predictions for unvalidated models."
            )

        model_path = Path(model_rel_path)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Trained model checkpoint bundle for '{crop}' not found on disk at {model_path}. "
                "Please run training or verify export."
            )

        # Load production bundle
        bundle = torch.load(model_path, map_location=self.device, weights_only=False)
        arch = bundle.get("architecture", crop_meta.get("architecture", "mobilenet_v3_small"))
        classes = bundle.get("classes", crop_meta.get("classes", []))
        input_resolution = bundle.get("input_resolution", [224, 224])

        # Instantiate model architecture and load weights
        model = create_model(arch, num_classes=len(classes), pretrained=False)
        model.load_state_dict(bundle["model_state_dict"])
        model.to(self.device)
        model.eval()

        # Find target layer for Grad-CAM
        if arch.startswith("mobilenet_v3"):
            gradcam_layer = model.features[-1]
        elif arch.startswith("resnet"):
            gradcam_layer = model.layer4[-1]
        else:
            gradcam_layer = list(model.children())[0]

        routed = RoutedModel(
            model=model,
            architecture=arch,
            crop=crop,
            category=category,
            classes=classes,
            input_resolution=input_resolution,
            gradcam_target_layer=gradcam_layer,
        )
        self.model_cache[cache_key] = routed
        logger.info(f"Loaded and cached model for {crop} ({arch}) on {self.device}")
        return routed
