"""Scientific model evaluation and benchmarking engine for AgriGuard AI."""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from agriguard.utils.logger import get_logger

logger = get_logger("evaluator")


class ModelEvaluator:
    def __init__(self, model: nn.Module, classes: List[str], device: str = "cpu"):
        self.model = model.to(device)
        self.model.eval()
        self.classes = sorted(classes)
        self.device = device

    @torch.no_grad()
    def evaluate(self, test_loader) -> Dict[str, Any]:
        all_preds = []
        all_targets = []
        all_probs = []
        latencies = []

        for images, targets in test_loader:
            images = images.to(self.device)
            start_t = time.perf_counter()
            outputs = self.model(images)
            latencies.append((time.perf_counter() - start_t) / images.size(0))

            probs = torch.softmax(outputs, dim=1)
            preds = torch.argmax(probs, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(targets.numpy())
            all_probs.extend(probs.cpu().numpy())

        all_preds = np.array(all_preds)
        all_targets = np.array(all_targets)

        acc = float(accuracy_score(all_targets, all_preds))
        macro_prec = float(precision_score(all_targets, all_preds, average="macro", zero_division=0))
        macro_rec = float(recall_score(all_targets, all_preds, average="macro", zero_division=0))
        macro_f1 = float(f1_score(all_targets, all_preds, average="macro", zero_division=0))
        weighted_f1 = float(f1_score(all_targets, all_preds, average="weighted", zero_division=0))

        cm = confusion_matrix(all_targets, all_preds, labels=range(len(self.classes))).tolist()
        clf_rep = classification_report(
            all_targets,
            all_preds,
            labels=list(range(len(self.classes))),
            target_names=self.classes,
            output_dict=True,
            zero_division=0,
        )

        avg_latency_ms = round(float(np.mean(latencies)) * 1000, 2) if latencies else 0.0

        eval_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "num_test_samples": len(all_targets),
            "classes": self.classes,
            "metrics": {
                "accuracy": round(acc, 4),
                "macro_precision": round(macro_prec, 4),
                "macro_recall": round(macro_rec, 4),
                "macro_f1": round(macro_f1, 4),
                "weighted_f1": round(weighted_f1, 4),
                "avg_latency_ms": avg_latency_ms,
            },
            "per_class_metrics": {
                c: {
                    "precision": round(clf_rep[c]["precision"], 4),
                    "recall": round(clf_rep[c]["recall"], 4),
                    "f1_score": round(clf_rep[c]["f1-score"], 4),
                    "support": clf_rep[c]["support"],
                }
                for c in self.classes
                if c in clf_rep
            },
            "confusion_matrix": cm,
        }
        return eval_data

    @staticmethod
    def generate_markdown_report(eval_data: Dict[str, Any], crop: str, arch: str) -> str:
        m = eval_data["metrics"]
        lines = [
            f"# Scientific Evaluation Report: {crop} ({arch})",
            f"**Evaluation Date:** {eval_data['timestamp']}  ",
            f"**Test Set Samples:** {eval_data['num_test_samples']}  ",
            "",
            "## Summary Performance",
            f"- **Overall Accuracy:** {m['accuracy']*100:.2f}%",
            f"- **Macro Precision:** {m['macro_precision']*100:.2f}%",
            f"- **Macro Recall:** {m['macro_recall']*100:.2f}%",
            f"- **Macro F1-Score:** {m['macro_f1']:.4f}",
            f"- **Weighted F1-Score:** {m['weighted_f1']:.4f}",
            f"- **Inference Latency (Avg):** {m['avg_latency_ms']} ms / sample",
            "",
            "## Per-Class Breakdown",
            "| Condition | Precision | Recall | F1-Score | Support |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for c, pm in eval_data["per_class_metrics"].items():
            lines.append(
                f"| `{c}` | {pm['precision']*100:.1f}% | {pm['recall']*100:.1f}% | {pm['f1_score']:.4f} | {pm['support']} |"
            )

        lines.extend([
            "",
            "## Confusion Matrix",
            f"Rows represent ground-truth classes; columns represent model predictions: {eval_data['classes']}",
            "",
            "```text",
        ])
        for row in eval_data["confusion_matrix"]:
            lines.append("  " + "  ".join(f"{val:>4d}" for val in row))
        lines.append("```")

        return "\n".join(lines)
