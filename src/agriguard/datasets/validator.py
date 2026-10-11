"""Image validation utility for dataset engineering and API upload verification."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageOps


@dataclass
class ValidationResult:
    is_valid: bool
    width: int = 0
    height: int = 0
    format: str = ""
    mode: str = ""
    error_message: Optional[str] = None


class ImageValidator:
    def __init__(
        self,
        min_width: int = 64,
        min_height: int = 64,
        max_dimension: int = 4096,
        allowed_formats: Optional[list[str]] = None,
        max_aspect_ratio: float = 3.5,
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.max_dimension = max_dimension
        self.allowed_formats = (
            [fmt.upper() for fmt in allowed_formats]
            if allowed_formats
            else ["JPEG", "JPG", "PNG", "WEBP"]
        )
        self.max_aspect_ratio = max_aspect_ratio

    def validate_file(self, file_path_or_buffer) -> ValidationResult:
        import io
        if isinstance(file_path_or_buffer, bytes):
            buffer = io.BytesIO(file_path_or_buffer)
        elif isinstance(file_path_or_buffer, io.BytesIO):
            buffer = file_path_or_buffer
        else:
            p = Path(file_path_or_buffer)
            if not p.is_file():
                return ValidationResult(is_valid=False, error_message="File does not exist")
            if p.stat().st_size == 0:
                return ValidationResult(is_valid=False, error_message="File is empty (0 bytes)")
            buffer = p

        try:
            with Image.open(buffer) as img:
                img_format = (img.format or "").upper()
                if img_format == "JPEG":
                    pass
                elif img_format not in self.allowed_formats and img_format != "JPG":
                    return ValidationResult(
                        is_valid=False,
                        format=img_format,
                        error_message=f"Unsupported format '{img_format}'. Allowed: {self.allowed_formats}",
                    )

                w, h = img.size
                if w < self.min_width or h < self.min_height:
                    return ValidationResult(
                        is_valid=False,
                        width=w,
                        height=h,
                        format=img_format,
                        error_message=f"Resolution {w}x{h} below minimum {self.min_width}x{self.min_height}",
                    )

                if w > self.max_dimension or h > self.max_dimension:
                    return ValidationResult(
                        is_valid=False,
                        width=w,
                        height=h,
                        format=img_format,
                        error_message=f"Resolution {w}x{h} exceeds maximum dimension {self.max_dimension}",
                    )

                aspect_ratio = max(w / max(h, 1), h / max(w, 1))
                if aspect_ratio > self.max_aspect_ratio:
                    return ValidationResult(
                        is_valid=False,
                        width=w,
                        height=h,
                        format=img_format,
                        error_message=f"Extreme aspect ratio {aspect_ratio:.2f} exceeds {self.max_aspect_ratio}",
                    )

                # Thorough verification of image data integrity
                img.verify()

            # Second pass to ensure raster image can actually be decompressed and converted to RGB
            if hasattr(buffer, "seek"):
                buffer.seek(0)
            with Image.open(buffer) as img2:
                img2 = ImageOps.exif_transpose(img2)
                _ = img2.convert("RGB")
                w, h = img2.size
                mode = img2.mode

            return ValidationResult(
                is_valid=True,
                width=w,
                height=h,
                format=img_format,
                mode=mode,
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Corrupt or unreadable image file: {str(e)}",
            )
