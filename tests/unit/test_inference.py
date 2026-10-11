"""Unit tests for inference pipeline and rejection mechanism."""

from pathlib import Path
from PIL import Image
import pytest

from agriguard.inference.pipeline import InferencePipeline
from agriguard.knowledge_base.service import KnowledgeBaseService
from agriguard.model_registry.router import ModelRouter


@pytest.fixture
def pipeline():
    router = ModelRouter(device="cpu")
    kb = KnowledgeBaseService()
    return InferencePipeline(
        router=router,
        kb_service=kb,
        confidence_threshold=0.50,
        entropy_ood_threshold=1.85,
        enable_gradcam=True,
    )


def test_real_inference_on_rice_leaf(pipeline):
    # Find a real downloaded rice_leaf image
    img_files = list(Path("data/raw/rice_leaf/bacterial_leaf_blight").glob("*.jpg")) + list(
        Path("data/raw/rice_leaf/bacterial_leaf_blight").glob("*.JPG")
    )
    assert len(img_files) > 0, "Expected downloaded test image"
    test_img = Image.open(img_files[0])

    res = pipeline.predict(
        image=test_img,
        category="grain_crop_leaf",
        crop="rice_leaf",
        return_gradcam=True,
    )

    assert "prediction_id" in res
    assert res["crop"] == "rice_leaf"
    assert res["category"] == "grain_crop_leaf"
    assert res["predicted_condition"] in ["bacterial_leaf_blight", "brown_spot", "leaf_smut"]
    assert 0.0 <= res["confidence"] <= 1.0
    if res["is_reliable"]:
        assert res["gradcam_heatmap"] is not None
    else:
        assert len(res["warnings"]) > 0
