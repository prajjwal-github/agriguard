"""Unit tests for agricultural knowledge base service."""

from agriguard.knowledge_base.service import KnowledgeBaseService


def test_kb_lookup_bacterial_leaf_blight():
    kb = KnowledgeBaseService()
    info = kb.get_info("rice_leaf", "bacterial_leaf_blight")
    assert info is not None
    assert info["disease_name"] == "Bacterial Leaf Blight"
    assert "Xanthomonas" in info["scientific_name"]
    assert len(info["prevention"]) > 0
    assert len(info["management"]) > 0
    assert "IRRI" in info["references"]


def test_kb_lookup_healthy():
    kb = KnowledgeBaseService()
    info = kb.get_info("rice_leaf", "healthy")
    assert info is not None
    assert info["pathogen_type"] == "None"


def test_kb_lookup_missing():
    kb = KnowledgeBaseService()
    info = kb.get_info("rice_leaf", "imaginary_disease_123")
    assert info is None
