"""Service for accessing and querying the verified agricultural disease knowledge base."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from agriguard.utils.logger import get_logger

logger = get_logger("knowledge_base")


class KnowledgeBaseService:
    def __init__(self, kb_path: str = "src/agriguard/knowledge_base/disease_kb.json"):
        self.kb_path = Path(kb_path)
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self):
        if not self.kb_path.exists():
            logger.warning(f"Knowledge base file not found at {self.kb_path}")
            self.data = {}
            return
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        logger.info(f"Loaded disease knowledge base for {len(self.data)} crops.")

    def get_info(self, crop: str, condition: str) -> Optional[Dict[str, Any]]:
        crop_data = self.data.get(crop, {})
        info = crop_data.get(condition)
        if not info:
            # Fallback check lowercase
            for k, v in crop_data.items():
                if k.lower() == condition.lower():
                    return v
        return info

    def get_crop_conditions(self, crop: str) -> list[str]:
        return list(self.data.get(crop, {}).keys())
