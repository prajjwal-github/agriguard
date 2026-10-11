"""Pydantic request and response schemas for AgriGuard AI API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    device: str
    timestamp: str


class CategoryItem(BaseModel):
    category_id: str
    display_name: str
    description: str
    supported_crops_count: int


class CropItem(BaseModel):
    crop_id: str
    display_name: str
    status: str  # ready, experimental, planned
    is_available: bool
    task: str
    classes: List[str]


class AlternativePrediction(BaseModel):
    condition: str
    display_name: str
    confidence: float


class SeverityResponse(BaseModel):
    supported: bool
    level: Optional[str] = None
    lesion_percentage: Optional[float] = None
    methodology: str
    notes: str


class ModelMetadataResponse(BaseModel):
    model_name: str
    architecture: str
    model_version: str
    device: str


class PredictionResponse(BaseModel):
    prediction_id: str
    category: str
    crop: str
    plant_part: str
    predicted_condition: str
    display_name: str
    is_reliable: bool
    confidence: float
    entropy: float
    alternative_predictions: List[AlternativePrediction]
    severity: SeverityResponse
    symptoms: str
    causes: str
    favorable_conditions: str
    prevention: List[str]
    management: List[str]
    consult_expert_when: str
    references: str
    model_metadata: ModelMetadataResponse
    gradcam_heatmap: Optional[str] = None  # Base64 JPEG string
    warnings: List[str]
    processing_time_ms: float


class CapabilitiesResponse(BaseModel):
    app_name: str
    version: str
    categories: Dict[str, CategoryItem]
    total_models_available: int
    allowed_formats: List[str]
    max_upload_size_mb: int
