"""Production inference and diagnosis pipeline for AgriGuard AI."""

import time
import uuid
from typing import Any, Dict, List, Optional
import numpy as np
from PIL import Image
import torch
import torchvision.transforms.functional as TF

from agriguard.explainability.gradcam import GradCAM
from agriguard.knowledge_base.service import KnowledgeBaseService
from agriguard.model_registry.router import ModelRouter, RoutedModel
from agriguard.preprocessing.transforms import get_eval_transforms
from agriguard.severity.estimator import SeverityEstimator
from agriguard.utils.logger import get_logger

logger = get_logger("inference_pipeline")


class InferencePipeline:
    def __init__(
        self,
        router: ModelRouter,
        kb_service: KnowledgeBaseService,
        confidence_threshold: float = 0.55,
        entropy_ood_threshold: float = 1.85,
        enable_gradcam: bool = True,
    ):
        self.router = router
        self.kb_service = kb_service
        self.confidence_threshold = confidence_threshold
        self.entropy_ood_threshold = entropy_ood_threshold
        self.enable_gradcam = enable_gradcam
        self.severity_estimator = SeverityEstimator()
        self.eval_transforms = get_eval_transforms((224, 224))

    def predict(
        self,
        image: Image.Image,
        category: str,
        crop: str,
        return_gradcam: bool = True,
    ) -> Dict[str, Any]:
        start_t = time.perf_counter()
        prediction_id = f"diag_{uuid.uuid4().hex[:10]}"

        # 1. Hierarchical Routing & Lazy Model Load
        routed: RoutedModel = self.router.route_and_load(category=category, crop=crop)

        # 2. Preprocessing
        rgb_img = image.convert("RGB")
        img_tensor = self.eval_transforms(rgb_img).unsqueeze(0).to(self.router.device)

        # 3. Model Inference
        with torch.no_grad():
            logits = routed.model(img_tensor)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

        # 4. Out-of-Distribution & Uncertainty Rejection Analysis
        # Shannon Entropy H(p) = -sum(p * log(p + eps))
        entropy = float(-np.sum(probs * np.log(probs + 1e-12)))
        top_idx = int(np.argmax(probs))
        top_confidence = float(probs[top_idx])
        top_condition = routed.classes[top_idx]

        warnings: List[str] = []
        is_reliable = True

        if top_confidence < self.confidence_threshold:
            is_reliable = False
            warnings.append(
                f"Confidence {top_confidence*100:.1f}% is below threshold {self.confidence_threshold*100:.1f}%. "
                "Unable to make a reliable diagnosis from this image. Please upload a clearer photograph of the selected crop or consult an agricultural expert."
            )

        if entropy > self.entropy_ood_threshold:
            is_reliable = False
            warnings.append(
                f"Prediction entropy ({entropy:.2f}) indicates high uncertainty or non-target image characteristics. "
                "The photograph may not clearly depict the selected crop or foliage."
            )

        # 5. Alternative Predictions
        sorted_indices = np.argsort(probs)[::-1]
        alternatives = []
        for rank, idx in enumerate(sorted_indices[:3]):
            cond_name = routed.classes[idx]
            cond_info = self.kb_service.get_info(crop, cond_name)
            alternatives.append({
                "condition": cond_name,
                "display_name": cond_info.get("disease_name", cond_name.replace("_", " ").title()) if cond_info else cond_name.replace("_", " ").title(),
                "confidence": round(float(probs[idx]), 4),
            })

        # 6. Grad-CAM Explainability
        gradcam_overlay_b64: Optional[str] = None
        if self.enable_gradcam and return_gradcam and is_reliable:
            try:
                gcam = GradCAM(routed.model, routed.gradcam_target_layer)
                heatmap = gcam.generate_heatmap(img_tensor, target_class_idx=top_idx)
                overlay = gcam.overlay_heatmap_on_image(rgb_img, heatmap)
                gradcam_overlay_b64 = gcam.to_base64_jpeg(overlay)
            except Exception as e:
                logger.warning(f"Grad-CAM generation failed: {e}")

        # 7. Severity Assessment
        plant_organ = "fruit_surface" if category in ["fruit", "vegetable"] else "leaf"
        if is_reliable:
            severity_res = self.severity_estimator.estimate(rgb_img, top_condition, plant_organ=plant_organ)
            severity_data = {
                "supported": severity_res.supported,
                "level": severity_res.severity_level,
                "lesion_percentage": severity_res.estimated_lesion_percentage,
                "methodology": severity_res.methodology,
                "notes": severity_res.notes,
            }
        else:
            severity_data = {
                "supported": False,
                "level": "Unavailable",
                "lesion_percentage": None,
                "methodology": "Not computed due to diagnostic uncertainty.",
                "notes": "Severity calculation requires a confident condition prediction.",
            }

        # 8. Knowledge Base & Agronomic Advice
        kb_info = self.kb_service.get_info(crop, top_condition) or {}
        display_name = kb_info.get("disease_name", top_condition.replace("_", " ").title())

        processing_time_ms = round((time.perf_counter() - start_t) * 1000, 2)

        return {
            "prediction_id": prediction_id,
            "category": category,
            "crop": crop,
            "plant_part": "fruit_surface" if category in ["fruit", "vegetable"] else "leaf",
            "predicted_condition": top_condition,
            "display_name": display_name,
            "is_reliable": is_reliable,
            "confidence": round(top_confidence, 4),
            "entropy": round(entropy, 4),
            "alternative_predictions": alternatives,
            "severity": severity_data,
            "symptoms": kb_info.get("symptoms", "No symptom descriptions registered."),
            "causes": kb_info.get("causes", "Pathogen cause details not documented."),
            "favorable_conditions": kb_info.get("favorable_conditions", "N/A"),
            "prevention": kb_info.get("prevention", []),
            "management": kb_info.get("management", []),
            "consult_expert_when": kb_info.get("consult_expert_when", "When symptoms persist or spread across >15% of the field."),
            "references": kb_info.get("references", "AgriGuard Agricultural Evidence Base."),
            "model_metadata": {
                "model_name": f"{crop}_{routed.architecture}",
                "architecture": routed.architecture,
                "model_version": "1.0.0",
                "device": self.router.device,
            },
            "gradcam_heatmap": gradcam_overlay_b64,
            "warnings": warnings,
            "processing_time_ms": processing_time_ms,
        }
