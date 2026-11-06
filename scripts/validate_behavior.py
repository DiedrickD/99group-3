import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.data import digest, load_notes, load_sources, read_jsonl


def main():
    notes, sources = load_notes(), load_sources()
    nmap = {n["note_id"]: n for n in notes}
    assert len(nmap) == len(notes) == 21
    assert len(sources) == 10
    assert all(n["source_id"] in sources for n in notes)
    train = read_jsonl(ROOT / "data/behavior_train.jsonl")
    broad = read_jsonl(ROOT / "data/behavior_broad_train.jsonl")
    validation = read_jsonl(ROOT / "data/behavior_validation.jsonl")
    assert len({r["id"] for r in train + broad}) == 56
    assert not {sid for r in train + broad for sid in r["source_ids"]} & {sid for r in validation for sid in r["source_ids"]}
    for row in train + broad + validation:
        assert all(nid in nmap for nid in row["note_ids"])
        assert set(row["source_ids"]) == {nmap[nid]["source_id"] for nid in row["note_ids"]}
    for filename in ["behavior_manifest.json", "behavior_broad_manifest.json"]:
        manifest = json.loads((ROOT / "data" / filename).read_text())
        for name, sha in manifest["sha256"].items():
            assert digest(ROOT / "data" / name) == sha
    for filename in ["training-behavior-stage1.json", "training-behavior.json"]:
        report = json.loads((ROOT / "reports" / filename).read_text())
        assert digest(ROOT / report["training_data_file"]) == report["training_data_sha256"]
        assert digest(ROOT / report["validation_data_file"]) == report["validation_data_sha256"]
    stage1 = json.loads((ROOT / "reports/training-behavior-stage1.json").read_text())
    assert stage1["parent_adapter_sha256"] == digest(ROOT / "models/lky-lora/adapter_model.safetensors")
    router = json.loads((ROOT / "models/router.json").read_text())
    assert router["training_data_sha256"] == digest(ROOT / "data/router_train.jsonl")
    artifact = json.loads((ROOT / "models/behavior_manifest.json").read_text())
    assert artifact["sha256"] == digest(ROOT / artifact["adapter_file"])
    assert artifact["parent_factual_adapter_sha256"] == stage1["parent_adapter_sha256"]
    stage2 = json.loads((ROOT / "reports/training-behavior.json").read_text())
    assert artifact["intermediate_stage1_sha256"] == stage2["parent_adapter_sha256"]
    for name, sha in artifact["reports_sha256"].items():
        assert digest(ROOT / name) == sha
    adapter = json.loads((ROOT / "models/lky-behavior/adapter_config.json").read_text())
    assert adapter["base_model_name_or_path"] == artifact["base_model"]["model_id"]
    assert adapter["revision"] == artifact["base_model"]["revision"]
    for name in ["behavior-baseline-v3.json", "behavior-lora-v3.json", "behavior-notes-v3.json"]:
        report = json.loads((ROOT / "reports" / name).read_text())
        assert report["dataset_sha256"] == digest(ROOT / "data/persona_eval.jsonl")
        assert report["persona_sha256"] == digest(ROOT / "data/persona.json")
        if report["behavior_adapter_sha256"]:
            assert report["behavior_adapter_sha256"] == artifact["sha256"]
    persona = json.loads((ROOT / "data/persona.json").read_text())
    assert all(p["note_id"] in nmap for p in persona["principles"])
    print("PASS: 10 sources, 21 notes, 56 unique behavior examples, source separation, data hashes and router lineage")


if __name__ == "__main__":
    main()
