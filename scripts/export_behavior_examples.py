"""Publish selected actual v3 outputs, including weak answers, for review."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.chat import render


def main():
    report = json.loads((ROOT / "reports/behavior-lora-v3.json").read_text(encoding="utf-8"))
    selected = {"chatgpt-false-premise", "earthquake", "leadership", "economic-crisis",
                "negotiation", "foreign-policy", "social-cohesion", "empty-corpus", "historical"}
    rows = [row for row in report["rows"] if row["case"]["id"] in selected]
    text = """# Recorded chat examples: behavior-trained model

These are actual local outputs of the factual or behavior LoRA adapter, selected
from [the complete 16-case report](../reports/behavior-lora-v3.json). The interface
renders historical precedents from the source notes and displays the model's
generated application separately. The unmodified model output remains in each
report row. Weak answers are retained: formatting is better, but recommendations
can be generic or miss the question. See [the quality review](QUALITY_REVIEW.md).

The model covers leadership, crises, negotiation, technology, foreign relations
and other domains; it does not reproduce Lee's private thoughts or establish his
views on modern events. [Training and architecture](BEHAVIOR.md),
[temporary live demo](DEMO.md), [original v1 examples](CHAT_EXAMPLES_V1.md).

"""
    for row in rows:
        result = row["result"]
        text += (f"## {row['case']['id']}\n\n**User:** {result['question']}\n\n"
                 f"Adapter: `{result.get('generation_adapter')}`; status: `{result['status']}`.\n\n"
                 + render(result) + "\n\n")
    (ROOT / "docs/CHAT_EXAMPLES.md").write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    (ROOT / "docs/chat_examples.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
                                                encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
