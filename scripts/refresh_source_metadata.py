"""Correct reference metadata without changing recorded generations or scores."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.data import load_sources, write_json


def main():
    sources = load_sources()
    for path in (ROOT / "reports").glob("eval-*.json"):
        report = json.loads(path.read_text(encoding="utf-8"))
        corrections = []
        for row in report["rows"]:
            for reference in row["result"]["references"]:
                source = sources[reference["source_id"]]
                if reference["locator"] != source["locator"]:
                    corrections.append({"case_id": row["case"]["id"], "source_id": reference["source_id"],
                                        "field": "locator", "before": reference["locator"], "after": source["locator"]})
                    reference["locator"] = source["locator"]
        if corrections:
            report.setdefault("reference_metadata_corrections", []).extend(corrections)
            write_json(path, report)
            print(f"{path.name}: corrected {len(corrections)} reference locators; generations and scores unchanged")


if __name__ == "__main__":
    main()
