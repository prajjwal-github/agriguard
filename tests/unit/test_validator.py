"""Unit tests for ImageValidator."""

import io
from PIL import Image
import pytest
from agriguard.datasets.validator import ImageValidator


def test_valid_image():
    validator = ImageValidator(min_width=64, min_height=64)
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")

    res = validator.validate_file(buf)
    assert res.is_valid is True
    assert res.width == 224
    assert res.height == 224
    assert res.format == "JPEG"


def test_empty_buffer():
    validator = ImageValidator()
    res = validator.validate_file(b"")
    assert res.is_valid is False


def test_corrupt_bytes():
    validator = ImageValidator()
    res = validator.validate_file(b"NOT_AN_IMAGE_RANDOM_GARBAGE_BYTES")
    assert res.is_valid is False
    assert "Corrupt or unreadable" in res.error_message


def test_too_small_resolution():
    validator = ImageValidator(min_width=64, min_height=64)
    img = Image.new("RGB", (32, 32), color=(0, 255, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    res = validator.validate_file(buf)
    assert res.is_valid is False
    assert "below minimum" in res.error_message
