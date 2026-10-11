"""
Synthetic Environmental Perturbation Test Suite.
Evaluates model stability against simulated optical/environmental distortions
(sunlight brightness +35%, canopy shadow -35%, Gaussian lens blur, high contrast).
NOTE: These are controlled synthetic transformations, distinct from in-situ real-world field trials.
"""

import glob
import numpy as np
import torch
from PIL import Image, ImageEnhance, ImageFilter

from agriguard.inference.pipeline import InferencePipeline
from agriguard.model_registry.router import ModelRouter
from agriguard.knowledge_base.service import KnowledgeBaseService

def test_environmental_perturbation_robustness():
    router = ModelRouter()
    pipeline = InferencePipeline(router=router, kb_service=KnowledgeBaseService())

    # Find sample test images from test manifest or raw
    test_samples = [
        ("fruit", "apple", glob.glob("data/raw/apple/rot_decay/*.jpg")[0]),
        ("fruit", "banana", glob.glob("data/raw/banana/rot_decay/*.jpg")[0]),
        ("fruit_leaf", "apple_leaf", glob.glob("data/raw/apple_leaf/apple_scab/*.[jJ][pP]*")[0]),
        ("vegetable_leaf", "tomato_leaf", glob.glob("data/raw/tomato_leaf/early_blight/*.[jJ][pP]*")[0]),
        ("grain_crop_leaf", "maize_leaf", glob.glob("data/raw/maize_leaf/common_rust/*.[jJ][pP]*")[0]),
    ]

    print("=== RUNNING SYNTHETIC ENVIRONMENTAL PERTURBATION TESTS (SIMULATED DISTORTIONS) ===")

    for cat, crop, img_path in test_samples:
        orig_img = Image.open(img_path).convert("RGB")
        base_res = pipeline.predict(orig_img, category=cat, crop=crop)
        base_pred = base_res["predicted_condition"]
        base_conf = base_res["confidence"]

        # Perturbation 1: Harsh Sunlight (+35% Brightness)
        enhancer = ImageEnhance.Brightness(orig_img)
        sunlight_img = enhancer.enhance(1.35)
        sun_res = pipeline.predict(sunlight_img, category=cat, crop=crop)

        # Perturbation 2: Deep Canopy Shadow (-35% Brightness)
        shadow_img = enhancer.enhance(0.65)
        shadow_res = pipeline.predict(shadow_img, category=cat, crop=crop)

        # Perturbation 3: Out-of-Focus Lens (Blur)
        blur_img = orig_img.filter(ImageFilter.GaussianBlur(radius=1.5))
        blur_res = pipeline.predict(blur_img, category=cat, crop=crop)

        # Perturbation 4: High Contrast (+40% Contrast)
        contrast_enhancer = ImageEnhance.Contrast(orig_img)
        contrast_img = contrast_enhancer.enhance(1.4)
        contrast_res = pipeline.predict(contrast_img, category=cat, crop=crop)

        # Check stability
        stability_count = sum([
            sun_res["predicted_condition"] == base_pred,
            shadow_res["predicted_condition"] == base_pred,
            blur_res["predicted_condition"] == base_pred,
            contrast_res["predicted_condition"] == base_pred,
        ])

        print(
            f"[{crop:12}] Base: '{base_pred}' ({base_conf*100:.1f}%) | "
            f"Sunlight: '{sun_res['predicted_condition']}' ({sun_res['confidence']*100:.1f}%) | "
            f"Shadow: '{shadow_res['predicted_condition']}' ({shadow_res['confidence']*100:.1f}%) | "
            f"Blur: '{blur_res['predicted_condition']}' ({blur_res['confidence']*100:.1f}%) | "
            f"Stability: {stability_count}/4 conditions"
        )
        assert stability_count >= 2, f"Model for {crop} too sensitive to optical perturbations"

    print("\n[ROBUSTNESS TEST PASSED]: Models maintain diagnosis stability under field perturbations.")

if __name__ == "__main__":
    test_environmental_perturbation_robustness()
