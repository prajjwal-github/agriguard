"""Generate comprehensive model coverage and evaluation report for all crops."""

import json
from pathlib import Path
import yaml


def generate_report():
    reports_dir = Path("data/reports")
    with open("configs/models.yaml", "r", encoding="utf-8") as f:
        models_cfg = yaml.safe_load(f)

    active_models = {}
    for cat_id, cat_info in models_cfg.get("categories", {}).items():
        for crop_id, crop_info in cat_info.get("crops", {}).items():
            if crop_info.get("status") == "ready" and crop_info.get("active_model"):
                arch = crop_info.get("architecture", "mobilenet_v3_small")
                active_models[crop_id] = {
                    "category": cat_id,
                    "display_name": crop_info.get("display_name"),
                    "architecture": arch,
                    "active_model": crop_info.get("active_model"),
                    "eval_file": reports_dir / f"evaluation_{crop_id}_{arch}.json",
                }

    summary = []
    for crop_id, meta in active_models.items():
        eval_path = meta["eval_file"]
        if not eval_path.exists():
            continue
        with open(eval_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        summary.append({
            "crop": crop_id,
            "display_name": meta["display_name"],
            "category": meta["category"],
            "architecture": meta["architecture"],
            "test_samples": data["num_test_samples"],
            "classes": data["classes"],
            "accuracy": data["metrics"]["accuracy"],
            "macro_f1": data["metrics"]["macro_f1"],
            "macro_precision": data["metrics"]["macro_precision"],
            "macro_recall": data["metrics"]["macro_recall"],
            "latency_ms": data["metrics"]["avg_latency_ms"],
        })

    out_json = reports_dir / "model_evaluation_summary.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Markdown format
    md_lines = [
        "# AgriGuard AI — Multi-Crop Scientific Model Evaluation Summary",
        "",
        "| Category | Crop | Architecture | Classes | Held-Out Test N | Accuracy | Macro F1 | Macro Prec | Macro Rec | Latency | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for s in summary:
        md_lines.append(
            f"| {s['category']} | **{s['display_name']}** (`{s['crop']}`) | `{s['architecture']}` | {len(s['classes'])} classes | {s['test_samples']} | "
            f"**{s['accuracy']*100:.1f}%** | {s['macro_f1']:.4f} | {s['macro_precision']:.4f} | "
            f"{s['macro_recall']:.4f} | {s['latency_ms']:.2f} ms | `Operational` |"
        )

    out_md = reports_dir / "model_evaluation_summary.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Model evaluation summary report written to {out_md}\n")
    for l in md_lines[2:]:
        print(l)


if __name__ == "__main__":
    generate_report()
