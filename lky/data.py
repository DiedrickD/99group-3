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
    return read_jsonl(ROOT / "data/notes.jsonl")


def load_sources():
    return {row["source_id"]: row for row in read_jsonl(ROOT / "data/sources.jsonl")}
