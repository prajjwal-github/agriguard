"""FastAPI application entrypoint for AgriGuard AI."""

import io
import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agriguard import __version__
from agriguard.api.schemas import (
    CapabilitiesResponse,
    CategoryItem,
    CropItem,
    HealthResponse,
    PredictionResponse,
)
from agriguard.config.settings import get_settings
from agriguard.datasets.validator import ImageValidator
from agriguard.inference.pipeline import InferencePipeline
from agriguard.knowledge_base.service import KnowledgeBaseService
from agriguard.model_registry.router import ModelRouter
from agriguard.utils.logger import get_logger

logger = get_logger("api_main")

settings = get_settings()

# State containers
_router: Optional[ModelRouter] = None
_kb_service: Optional[KnowledgeBaseService] = None
_pipeline: Optional[InferencePipeline] = None
_validator: Optional[ImageValidator] = None


def get_router() -> ModelRouter:
    global _router
    if _router is None:
        _router = ModelRouter(device=settings.default_device)
    return _router


def get_kb_service() -> KnowledgeBaseService:
    global _kb_service
    if _kb_service is None:
        _kb_service = KnowledgeBaseService()
    return _kb_service


def get_validator() -> ImageValidator:
    global _validator
    if _validator is None:
        _validator = ImageValidator()
    return _validator


def get_pipeline() -> InferencePipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = InferencePipeline(
            router=get_router(),
            kb_service=get_kb_service(),
            confidence_threshold=settings.confidence_threshold,
            entropy_ood_threshold=settings.ood_entropy_threshold,
            enable_gradcam=True,
        )
    return _pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AgriGuard AI backend services...")
    get_pipeline()
    logger.info("AgriGuard AI backend services initialized successfully.")
    yield
    logger.info("Shutting down AgriGuard AI backend...")


app = FastAPI(
    title="AgriGuard AI API",
    description="Scientific Multi-Crop Agricultural Disease Detection and Health Intelligence API",
    version=__version__,
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Service health and operational status check."""
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=__version__,
        device=settings.default_device,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/api/v1/categories", response_model=Dict[str, CategoryItem], tags=["Taxonomy"])
async def get_categories():
    """Retrieve all supported primary agricultural categories."""
    r = get_router()
    return r.get_categories()


@app.get("/api/v1/crops/{category_id}", response_model=List[CropItem], tags=["Taxonomy"])
async def get_crops(category_id: str):
    """Retrieve all registered crops and model readiness states for a category."""
    r = get_router()
    try:
        return r.get_crops_by_category(category_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/api/v1/capabilities", response_model=CapabilitiesResponse, tags=["System"])
async def get_capabilities():
    """Retrieve platform capabilities, format allowances, and active models."""
    r = get_router()
    categories = r.get_categories()

    total_available = 0
    for cat_id in categories:
        crops = r.get_crops_by_category(cat_id)
        total_available += sum(1 for c in crops if c["is_available"])

    return CapabilitiesResponse(
        app_name=settings.app_name,
        version=__version__,
        categories=categories,
        total_models_available=total_available,
        allowed_formats=settings.allowed_image_formats,
        max_upload_size_mb=settings.max_upload_size_mb,
    )


@app.get("/api/v1/evaluations", tags=["Transparency"])
async def get_evaluation_reports():
    """Retrieve verified evaluation metrics and benchmarks for transparency."""
    rep_dir = Path("data/reports")
    reports = {}
    if rep_dir.exists():
        for f in rep_dir.glob("evaluation_*.json"):
            try:
                with open(f, "r", encoding="utf-8") as rf:
                    reports[f.stem.replace("evaluation_", "")] = json.load(rf)
            except Exception:
                pass
    return reports


@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Inference"])
async def predict_crop_disease(
    category: str = Form(..., description="Selected primary category (e.g., fruit_leaf, grain_crop_leaf)"),
    crop: str = Form(..., description="Selected crop identifier (e.g., rice_leaf, apple_leaf)"),
    file: UploadFile = File(..., description="Photograph of the crop, plant organ, or leaf"),
):
    """
    Perform authenticated crop disease inference with OOD rejection, Grad-CAM,
    and verified agronomic management recommendations.
    """
    pipe = get_pipeline()
    val = get_validator()

    # 1. File size validation
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Uploaded file exceeds {settings.max_upload_size_mb} MB limit.",
        )
    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty (0 bytes).",
        )

    # 2. Image integrity and format verification
    try:
        pil_img = Image.open(io.BytesIO(content))
        v_res = val.validate_file(io.BytesIO(content))
        # Reset stream read or pass PIL image directly
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted image file: {str(e)}",
        )

    # 3. Model Routing & Execution
    try:
        result = pipe.predict(
            image=pil_img,
            category=category,
            crop=crop,
            return_gradcam=True,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.exception("Inference error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(e)}",
        )
