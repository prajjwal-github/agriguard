"""Dataset auditing and quality readiness gate engine for AgriGuard AI."""

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class QualityGateResult:
    passed: bool
    warnings: List[str]
    failures: List[str]


class DatasetAuditor:
    def __init__(
        self,
        min_samples_per_class: int = 15,
        max_imbalance_ratio: float = 10.0,
        min_split_train_ratio: float = 0.50,
    ):
        self.min_samples_per_class = min_samples_per_class
        self.max_imbalance_ratio = max_imbalance_ratio
        self.min_split_train_ratio = min_split_train_ratio

    def audit(
        self,
        crop: str,
        category: str,
        records: List[Dict],
        corrupt_count: int = 0,
        duplicate_count: int = 0,
        leakage_violations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        total_usable = len(records)
        class_counts = Counter(r.get("condition") for r in records)
        split_counts = Counter(r.get("split") for r in records)

        widths = [r.get("width", 0) for r in records if r.get("width")]
        heights = [r.get("height", 0) for r in records if r.get("height")]

        # Imbalance calculation
        if class_counts:
            min_c = min(class_counts.values())
            max_c = max(class_counts.values())
            imbalance_ratio = round(max_c / max(min_c, 1), 2)
        else:
            min_c, max_c, imbalance_ratio = 0, 0, 0.0

        # Evaluate quality gates
        warnings = []
        failures = []

        if total_usable == 0:
            failures.append("Dataset has zero usable samples.")
        for cls, count in class_counts.items():
            if count < self.min_samples_per_class:
                warnings.append(
                    f"Class '{cls}' has only {count} samples (recommended >= {self.min_samples_per_class})"
                )

        if imbalance_ratio > self.max_imbalance_ratio:
            warnings.append(
                f"Severe class imbalance ratio {imbalance_ratio}:1 exceeds limit {self.max_imbalance_ratio}:1"
            )

        if corrupt_count > (total_usable + corrupt_count) * 0.15:
            warnings.append(f"High corruption rate: {corrupt_count} corrupt files detected")

        if leakage_violations:
            for viol in leakage_violations:
                failures.append(f"Data leakage failure: {viol}")

        passed = len(failures) == 0

        audit_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "crop": crop,
            "category": category,
            "total_images": total_usable + corrupt_count + duplicate_count,
            "usable_images": total_usable,
            "corrupt_images": corrupt_count,
            "duplicate_images": duplicate_count,
            "num_classes": len(class_counts),
            "class_distribution": dict(class_counts),
            "split_distribution": dict(split_counts),
            "imbalance_ratio": imbalance_ratio,
            "resolution_stats": {
                "min_width": min(widths) if widths else 0,
                "max_width": max(widths) if widths else 0,
                "avg_width": round(sum(widths) / len(widths), 1) if widths else 0,
                "min_height": min(heights) if heights else 0,
                "max_height": max(heights) if heights else 0,
                "avg_height": round(sum(heights) / len(heights), 1) if heights else 0,
            },
            "quality_gate": {
                "passed": passed,
                "warnings": warnings,
                "failures": failures,
            },
        }
        return audit_data

    @staticmethod
    def generate_markdown_report(audit_data: Dict[str, Any]) -> str:
        qg = audit_data["quality_gate"]
        status_badge = "✅ PASSED" if qg["passed"] else "❌ FAILED"
        lines = [
            f"# Dataset Audit Report: {audit_data['crop']} ({audit_data['category']})",
            f"**Audit Timestamp:** {audit_data['timestamp']}  ",
            f"**Quality Gate Status:** {status_badge}  ",
            "",
            "## Summary Metrics",
            f"- **Total Recorded Samples:** {audit_data['total_images']}",
            f"- **Usable Samples:** {audit_data['usable_images']}",
            f"- **Corrupt / Unreadable Images:** {audit_data['corrupt_images']}",
            f"- **Duplicates Identified:** {audit_data['duplicate_images']}",
            f"- **Total Classes:** {audit_data['num_classes']}",
            f"- **Class Imbalance Ratio:** {audit_data['imbalance_ratio']}:1",
            "",
            "## Class Distribution",
            "| Condition / Class | Sample Count | Percentage |",
            "| :--- | :--- | :--- |",
        ]
        total_u = max(audit_data["usable_images"], 1)
        for cls, count in audit_data["class_distribution"].items():
            pct = round((count / total_u) * 100, 1)
            lines.append(f"| `{cls}` | {count} | {pct}% |")

        lines.extend([
            "",
            "## Split Breakdown",
            "| Split | Sample Count | Share |",
            "| :--- | :--- | :--- |",
        ])
        for sp, count in audit_data["split_distribution"].items():
            pct = round((count / total_u) * 100, 1)
            lines.append(f"| `{sp}` | {count} | {pct}% |")

        lines.extend([
            "",
            "## Resolution Statistics",
            f"- **Width:** Min {audit_data['resolution_stats']['min_width']}px, Avg {audit_data['resolution_stats']['avg_width']}px, Max {audit_data['resolution_stats']['max_width']}px",
            f"- **Height:** Min {audit_data['resolution_stats']['min_height']}px, Avg {audit_data['resolution_stats']['avg_height']}px, Max {audit_data['resolution_stats']['max_height']}px",
            "",
            "## Quality Gate Findings",
        ])
        if not qg["warnings"] and not qg["failures"]:
            lines.append("No warnings or failures. Dataset meets all production criteria.")
        else:
            if qg["failures"]:
                lines.append("### Critical Failures:")
                for f in qg["failures"]:
                    lines.append(f"- ❌ {f}")
            if qg["warnings"]:
                lines.append("### Warnings:")
                for w in qg["warnings"]:
                    lines.append(f"- ⚠️ {w}")

        return "\n".join(lines)
