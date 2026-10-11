"""Unit tests for ModelRouter and hierarchical routing."""

import pytest
from agriguard.model_registry.router import ModelRouter


@pytest.fixture
def router():
    return ModelRouter(registry_config_path="configs/models.yaml", device="cpu")


def test_get_categories(router):
    cats = router.get_categories()
    assert len(cats) == 6
    assert "fruit" in cats
    assert "fruit_leaf" in cats
    assert "vegetable" in cats
    assert "vegetable_leaf" in cats
    assert "grain" in cats
    assert "grain_crop_leaf" in cats


def test_crops_for_category(router):
    crops = router.get_crops_by_category("grain_crop_leaf")
    crop_ids = [c["crop_id"] for c in crops]
    assert "rice_leaf" in crop_ids
    assert "maize_leaf" in crop_ids


def test_invalid_category_raises(router):
    with pytest.raises(ValueError, match="does not exist"):
        router.get_crops_by_category("non_existent_category")


def test_cross_category_routing_rejected(router):
    # Attempting to load rice_leaf under fruit category must fail
    with pytest.raises(ValueError, match="not registered under category"):
        router.route_and_load(category="fruit", crop="rice_leaf")


def test_unsupported_planned_crop_rejected(router):
    # Attempting to load wheat_leaf (which is planned, not yet operational)
    with pytest.raises(ValueError, match="active development"):
        router.route_and_load(category="grain_crop_leaf", crop="wheat_leaf")


def test_valid_crop_loads(router):
    routed = router.route_and_load(category="grain_crop_leaf", crop="rice_leaf")
    assert routed.crop == "rice_leaf"
    assert routed.category == "grain_crop_leaf"
    assert len(routed.classes) == 3
    assert "bacterial_leaf_blight" in routed.classes
