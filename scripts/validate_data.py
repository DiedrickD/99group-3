import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.data import read_jsonl, digest
import json


def main():
    sources = read_jsonl(ROOT / "data/sources.jsonl")
    notes = read_jsonl(ROOT / "data/notes.jsonl")
    train = read_jsonl(ROOT / "data/train.jsonl")
    validation = read_jsonl(ROOT / "data/validation.jsonl")
    evaluation = read_jsonl(ROOT / "data/eval.jsonl")
    assert len({r["source_id"] for r in sources}) == len(sources)
    assert len({r["note_id"] for r in notes}) == len(notes)
    smap = {r["source_id"]: r for r in sources}
    nmap = {r["note_id"]: r for r in notes}
    assert all(urlparse(r["url"]).hostname in {"www.pmo.gov.sg", "www.nas.gov.sg", "www.mfa.gov.sg"} for r in sources)
    assert all(r["source_id"] in smap for r in notes)
    for row in train + validation:
        assert all(nid in nmap for nid in row["note_ids"])
        assert set(row["source_ids"]) == {nmap[nid]["source_id"] for nid in row["note_ids"]}
    train_sources = {sid for r in train for sid in r["source_ids"]}
    valid_sources = {sid for r in validation for sid in r["source_ids"]}
    assert not train_sources & valid_sources
    assert "S08" not in train_sources | valid_sources
    assert not {r["question"].casefold() for r in train} & {r["question"].casefold() for r in evaluation}
    for row in evaluation:
        assert all(nid in nmap for nid in row["relevant_note_ids"])
        assert row["expected_abstain"] == (not row["relevant_note_ids"])
    manifest = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
    for name, sha in manifest["sha256"].items():
        assert digest(ROOT / "data" / name) == sha, name
    print("PASS: source links, provenance, unique IDs, source splits, exact question separation and hashes")


if __name__ == "__main__":
    main()
