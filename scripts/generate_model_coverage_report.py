"""Generate comprehensive model coverage and evaluation report for all crops."""

import json
from pathlib import Path

def generate_report():
    reports_dir = Path("data/reports")
    json_files = sorted(list(reports_dir.glob("evaluation_*.json")))

    summary = []
    for jf in json_files:
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        crop_id = jf.stem.replace("evaluation_", "").replace("_mobilenet_v3_small", "")
        summary.append({
            "crop": crop_id,
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
        "| Crop | Task / Organ | Classes | Isolated Test N | Accuracy | Macro F1 | Macro Prec | Macro Rec | CPU Latency | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for s in summary:
        md_lines.append(
            f"| **{s['crop']}** | Classification | {len(s['classes'])} classes | {s['test_samples']} | "
            f"**{s['accuracy']*100:.1f}%** | {s['macro_f1']:.4f} | {s['macro_precision']:.4f} | "
            f"{s['macro_recall']:.4f} | {s['latency_ms']:.2f} ms | `Operational` |"
        )

    out_md = reports_dir / "model_evaluation_summary.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Model evaluation summary report written to {out_md}")
    for l in md_lines[2:]:
        print(l)

if __name__ == "__main__":
    generate_report()
