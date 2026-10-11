"""Discover and verify available public agricultural datasets."""

import argparse
import json
import sys
from pathlib import Path
import requests
import yaml

from agriguard.utils.logger import get_logger

logger = get_logger("discover_datasets")


def discover_datasets(sources_path: str = "datasets/sources.yaml", output_path: str = "data/reports/discovery_report.json"):
    sources_file = Path(sources_path)
    if not sources_file.exists():
        logger.error(f"Sources file not found: {sources_file}")
        sys.exit(1)

    with open(sources_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sources = data.get("sources", [])
    logger.info(f"Discovered {len(sources)} registered dataset sources in {sources_path}.")

    report = []
    for src in sources:
        src_id = src.get("id")
        name = src.get("name")
        url = src.get("source_url")
        license_type = src.get("license")
        logger.info(f"Checking dataset [{src_id}]: {name}")
        logger.info(f"  URL: {url} | License: {license_type}")

        reachable = False
        status_code = None
        try:
            res = requests.head(url, timeout=10, allow_redirects=True)
            status_code = res.status_code
            reachable = res.status_code < 400
        except Exception as e:
            logger.warning(f"  Connection check warning: {e}")

        info = {
            "id": src_id,
            "name": name,
            "url": url,
            "license": license_type,
            "reachable": reachable,
            "http_status": status_code,
            "crop_coverage": src.get("crop", src.get("crops")),
            "known_limitations": src.get("known_limitations"),
        }
        report.append(info)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Discovery report successfully saved to {out_file}")


def main():
    parser = argparse.ArgumentParser(description="Discover registered agricultural datasets")
    parser.add_argument("--sources", default="datasets/sources.yaml", help="Path to sources.yaml")
    parser.add_argument("--output", default="data/reports/discovery_report.json", help="Report output path")
    args = parser.parse_args()

    discover_datasets(args.sources, args.output)


if __name__ == "__main__":
    main()
