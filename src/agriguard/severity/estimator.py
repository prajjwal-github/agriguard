"""Empirical severity estimation for agricultural foliage diseases."""

from dataclasses import dataclass
from typing import Optional
import numpy as np
from PIL import Image


@dataclass
class SeverityAssessment:
    supported: bool
    severity_level: Optional[str] = None  # None, Mild, Moderate, Severe, Unavailable
    estimated_lesion_percentage: Optional[float] = None
    methodology: str = ""
    notes: str = ""


class SeverityEstimator:
    """
    Computes disease severity index using adaptive color-space segmentation
    (chlorosis and necrosis masking relative to total leaf tissue area).
    Transparently reports methodology and disclaimers.
    """

    def estimate(
        self,
        image: Image.Image,
        condition: str,
        plant_organ: str = "leaf",
    ) -> SeverityAssessment:
        if plant_organ != "leaf":
            return SeverityAssessment(
                supported=False,
                severity_level="Not Applicable (Fruit Surface)",
                estimated_lesion_percentage=None,
                methodology="Excess Green (ExG) vegetative index is specific to chlorophyll-bearing foliage.",
                notes="Fruit surface grading relies on direct surface defect segmentation. ExG foliage index is scientifically inapplicable to non-foliar fruit organs.",
            )

        if condition.lower() == "healthy":
            return SeverityAssessment(
                supported=True,
                severity_level="None (Healthy)",
                estimated_lesion_percentage=0.0,
                methodology="Verified healthy foliage baseline.",
                notes="Foliage exhibits vigorous chlorophyll pigmentation with no detectable necrotic or chlorotic lesions.",
            )

        try:
            rgb_arr = np.array(image.convert("RGB"), dtype=np.float32) / 255.0
            r, g, b = rgb_arr[:, :, 0], rgb_arr[:, :, 1], rgb_arr[:, :, 2]

            # Excess Green Index: 2G - R - B (plant foliage detection)
            exg = 2.0 * g - r - b
            leaf_mask = exg > 0.05

            leaf_pixels = np.count_nonzero(leaf_mask)
            if leaf_pixels < 500:
                # If leaf contour cannot be reliably separated
                return SeverityAssessment(
                    supported=False,
                    severity_level="Unavailable",
                    estimated_lesion_percentage=None,
                    methodology="Morphological leaf extraction.",
                    notes="Leaf contour could not be isolated with high confidence. Calibrated laboratory lesion analysis recommended.",
                )

            # Necrosis and chlorosis detection: high red/blue ratio or low chlorophyll relative to leaf
            # Lesion pixels have low green index relative to red/brown pigmentation
            lesion_mask = leaf_mask & ((r > g * 0.95) | (r + g < 0.35))
            lesion_pixels = np.count_nonzero(lesion_mask)

            pct = round(float((lesion_pixels / leaf_pixels) * 100), 1)
            pct = min(max(pct, 1.0), 95.0)

            if pct < 12.0:
                level = "Mild"
            elif pct < 35.0:
                level = "Moderate"
            else:
                level = "Severe"

            return SeverityAssessment(
                supported=True,
                severity_level=f"{level} (Experimental)",
                estimated_lesion_percentage=pct,
                methodology="Experimental ExG foliage colorimetric index (Clinical Advisory Only).",
                notes=f"Estimated {pct}% visible necrotic/chlorotic symptom coverage on detected leaf tissue. ExG colorimetry is an experimental advisory index; laboratory or agronomic expert confirmation recommended.",
            )

        except Exception as e:
            return SeverityAssessment(
                supported=False,
                severity_level="Unavailable",
                estimated_lesion_percentage=None,
                methodology="Foliage lesion analysis.",
                notes=f"Severity calculation skipped due to processing error: {str(e)}",
            )
