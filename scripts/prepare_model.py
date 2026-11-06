"""Resolve an immutable model revision, then download it without executing remote code."""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.data import write_json


def main():
    from huggingface_hub import HfApi, snapshot_download
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id", default="Qwen/Qwen2.5-0.5B-Instruct",
                        choices=["Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct"])
    parser.add_argument("--revision", default="main")
    args = parser.parse_args()
    info = HfApi().model_info(args.model_id, revision=args.revision)
    config = {"model_id": args.model_id, "revision": info.sha, "license": "apache-2.0",
              "model_card": f"https://huggingface.co/{args.model_id}",
              "resolved_date": datetime.now(timezone.utc).date().isoformat()}
    # Save only after a successful download, so a failed run cannot break inference.
    local_directory = "models/base/" + args.model_id.replace("/", "--")
    config["local_directory"] = local_directory
    snapshot_download(args.model_id, revision=info.sha, local_dir=ROOT / local_directory,
                      allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "*.tiktoken"])
    write_json(ROOT / "config/model.json", config)
    print(config)


if __name__ == "__main__":
    main()
