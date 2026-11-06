"""Check that published artifacts are complete and match the recorded dataset."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.data import digest


def main():
    required = ["README.md", "docs/DATASET.md", "docs/WORKFLOW.md", "docs/EVALUATION.md",
                "docs/MODEL_CARD.md", "docs/SUBMISSION.md", "docs/CHAT_EXAMPLES.md", "docs/RESULTS.md",
                "models/lky-lora/adapter_model.safetensors", "models/lky-lora/adapter_config.json",
                "reports/training.json", "notebooks/train_colab.ipynb"]
    assert all((ROOT / path).is_file() for path in required)
    training = json.loads((ROOT / "reports/training.json").read_text(encoding="utf-8"))
    assert training["training_data_sha256"] == digest(ROOT / "data/train.jsonl")
    assert training["validation_data_sha256"] == digest(ROOT / "data/validation.jsonl")
    adapter = json.loads((ROOT / "models/lky-lora/adapter_config.json").read_text(encoding="utf-8"))
    assert adapter["base_model_name_or_path"] == training["base_model"]["model_id"]
    assert adapter["revision"] == training["base_model"]["revision"]
    model_manifest = json.loads((ROOT / "models/manifest.json").read_text(encoding="utf-8"))
    assert model_manifest["sha256"] == digest(ROOT / model_manifest["adapter_file"])
    for name in ["notes", "base-rag", "lora-rag", "base-no-rag", "lora-no-rag"]:
        report = json.loads((ROOT / f"reports/eval-{name}.json").read_text(encoding="utf-8"))
        assert report["cases"] == 22
        assert report["eval_data_sha256"] == digest(ROOT / "data/eval.jsonl")
        assert report["notes_sha256"] == digest(ROOT / "data/notes.jsonl")
    notebook = json.loads((ROOT / "notebooks/train_colab.ipynb").read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            compile("".join(cell["source"]), "colab-cell", "exec")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "base" in path.parts:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
            if "://" in target or target.startswith("#") or " " in target:
                continue
            local = target.split("#")[0]
            assert (path.parent / local).exists(), (str(path), target)
    print("PASS: published files, adapter lineage, training/evaluation hashes and notebook code syntax")


if __name__ == "__main__":
    main()
