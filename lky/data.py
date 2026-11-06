import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_notes():
    notes = read_jsonl(ROOT / "data/notes.jsonl")
    for name in ["behavior_notes.jsonl", "extended_notes.jsonl"]:
        extra = ROOT / "data" / name
        if extra.exists():
            notes += read_jsonl(extra)
    return notes


def load_sources():
    sources = read_jsonl(ROOT / "data/sources.jsonl")
    for name in ["behavior_sources.jsonl", "extended_sources.jsonl"]:
        extra = ROOT / "data" / name
        if extra.exists():
            sources += read_jsonl(extra)
    return {row["source_id"]: row for row in sources}
