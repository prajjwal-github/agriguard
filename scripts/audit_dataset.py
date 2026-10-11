"""Perform comprehensive dataset audit and generate quality readiness reports."""

import argparse
import json
from collections import defaultdict
from pathlib import Path

from agriguard.datasets.auditor import DatasetAuditor
from agriguard.datasets.registry import DatasetRegistry
from agriguard.utils.logger import get_logger

logger = get_logger("audit_dataset")


def audit_dataset(manifests_dir: str = "data/manifests", reports_dir: str = "data/reports"):
    registry = DatasetRegistry(manifests_dir)
    records = registry.load_manifest()

    if not records:
        logger.error("No records in manifest. Run generate_manifest first.")
        return

    rep_path = Path(reports_dir)
    rep_path.mkdir(parents=True, exist_ok=True)

    auditor = DatasetAuditor(min_samples_per_class=10, max_imbalance_ratio=8.0)
    crop_groups = defaultdict(list)
    for r in records:
        crop_groups[r["crop"]].append(r)

    overall_audits = {}
    for crop, c_records in crop_groups.items():
        category = c_records[0].get("category", "unknown")
        audit_res = auditor.audit(crop=crop, category=category, records=c_records)
        overall_audits[crop] = audit_res

        # Write crop-specific markdown report
        md_content = auditor.generate_markdown_report(audit_res)
        md_file = rep_path / f"dataset_audit_{crop}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(
            f"Audit for '{crop}': Samples={audit_res['usable_images']}, "
            f"Classes={audit_res['num_classes']}, Imbalance={audit_res['imbalance_ratio']}:1, "
            f"Quality Gate={'PASSED' if audit_res['quality_gate']['passed'] else 'WARNINGS'}"
        )

    # Save summary JSON
    summary_file = rep_path / "dataset_audit_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(overall_audits, f, indent=2)

    logger.info(f"Dataset audit reports saved in {rep_path}")


def main():
    parser = argparse.ArgumentParser(description="Audit dataset quality and produce reports")
    parser.add_argument("--manifests-dir", default="data/manifests", help="Manifests directory")
    parser.add_argument("--reports-dir", default="data/reports", help="Reports directory")
    args = parser.parse_args()

    audit_dataset(args.manifests_dir, args.reports_dir)


if __name__ == "__main__":
    main()
