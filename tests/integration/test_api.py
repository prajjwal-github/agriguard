"""Integration tests for AgriGuard FastAPI endpoints."""

import io
from pathlib import Path
from PIL import Image
import pytest
from httpx import ASGITransport, AsyncClient

from agriguard.api.main import app


@pytest.mark.anyio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["app_name"] == "AgriGuard AI"


@pytest.mark.anyio
async def test_categories_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/categories")
        assert res.status_code == 200
        cats = res.json()
        assert len(cats) == 6
        assert "grain_crop_leaf" in cats


@pytest.mark.anyio
async def test_crops_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/crops/grain_crop_leaf")
        assert res.status_code == 200
        crops = res.json()
        crop_ids = [c["crop_id"] for c in crops]
        assert "rice_leaf" in crop_ids


@pytest.mark.anyio
async def test_capabilities_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/capabilities")
        assert res.status_code == 200
        data = res.json()
        assert data["total_models_available"] >= 1


@pytest.mark.anyio
async def test_predict_endpoint_with_real_image():
    # Load an authentic rice leaf image
    img_files = list(Path("data/raw/rice_leaf/bacterial_leaf_blight").glob("*.jpg")) + list(
        Path("data/raw/rice_leaf/bacterial_leaf_blight").glob("*.JPG")
    )
    assert len(img_files) > 0
    with open(img_files[0], "rb") as f:
        img_bytes = f.read()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        files = {"file": ("test_leaf.jpg", img_bytes, "image/jpeg")}
        data = {"category": "grain_crop_leaf", "crop": "rice_leaf"}

        res = await client.post("/api/v1/predict", files=files, data=data)
        assert res.status_code == 200
        pred = res.json()
        assert pred["crop"] == "rice_leaf"
        assert pred["predicted_condition"] in ["bacterial_leaf_blight", "brown_spot", "leaf_smut"]
        assert "symptoms" in pred
        assert "management" in pred
        assert pred["model_metadata"]["architecture"] == "mobilenet_v3_small"
