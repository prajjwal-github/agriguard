"""Centralized configuration loader for AgriGuard AI."""

import os
from pathlib import Path
from typing import Any, Dict
import yaml
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    app_name: str = "AgriGuard AI"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]
    max_upload_size_mb: int = 10
    allowed_image_formats: list[str] = ["jpeg", "jpg", "png", "webp"]
    default_device: str = "cpu"
    confidence_threshold: float = 0.55
    ood_entropy_threshold: float = 1.85


def load_yaml(path: str | Path) -> Dict[str, Any]:
    """Safely loads a YAML configuration file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Configuration file not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_settings() -> AppSettings:
    """Instantiates application settings with environment overrides."""
    origins_env = os.getenv("ALLOWED_ORIGINS")
    allowed_origins = (
        [o.strip() for o in origins_env.split(",") if o.strip()]
        if origins_env
        else ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    )

    return AppSettings(
        app_name=os.getenv("APP_NAME", "AgriGuard AI"),
        app_env=os.getenv("APP_ENV", "development"),
        api_host=os.getenv("API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("API_PORT", 8000)),
        allowed_origins=allowed_origins,
        max_upload_size_mb=int(os.getenv("MAX_UPLOAD_SIZE_MB", 10)),
        default_device=os.getenv("DEFAULT_DEVICE", "cpu"),
        confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", 0.55)),
        ood_entropy_threshold=float(os.getenv("OOD_ENTROPY_THRESHOLD", 1.85)),
    )
