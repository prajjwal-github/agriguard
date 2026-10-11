"""End-to-end smoke test for AgriGuard AI platform."""

from pathlib import Path
from PIL import Image
import torch

from agriguard.inference.pipeline import InferencePipeline
from agriguard.knowledge_base.service import KnowledgeBaseService
from agriguard.model_registry.router import ModelRouter


def test_smoke_end_to_end_prediction():
    # 1. Verify model bundle exists
    bundle_path = Path("models/exported/rice_leaf_mobilenet_v3_small.pt")
    assert bundle_path.exists(), f"Model bundle {bundle_path} does not exist"

    # 2. Verify router loads bundle
    router = ModelRouter(device="cpu")
    routed = router.route_and_load("grain_crop_leaf", "rice_leaf")
    assert routed is not None
    assert routed.crop == "rice_leaf"

    # 3. Load sample image
    sample_files = list(Path("data/raw/rice_leaf/bacterial_leaf_blight").glob("*.jpg")) + list(
        Path("data/raw/rice_leaf/bacterial_leaf_blight").glob("*.JPG")
    )
    assert len(sample_files) > 0, "No raw rice leaf sample files found"
    img = Image.open(sample_files[0])

    # 4. Run inference
    pipeline = InferencePipeline(
        router=router,
        kb_service=KnowledgeBaseService(),
        confidence_threshold=0.45,
    )
    result = pipeline.predict(image=img, category="grain_crop_leaf", crop="rice_leaf")

    assert "prediction_id" in result
    assert result["crop"] == "rice_leaf"
    assert result["predicted_condition"] in ["bacterial_leaf_blight", "brown_spot", "leaf_smut"]
    assert "symptoms" in result
    assert "management" in result
    print("\n[SMOKE TEST SUCCESS] Predicted:", result["predicted_condition"], "Confidence:", result["confidence"])
