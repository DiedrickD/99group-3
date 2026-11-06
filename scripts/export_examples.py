"""Publish original v1 outputs separately from current behavior examples."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.chat import render
from lky.data import write_json


def main():
    report_path = ROOT / "reports/eval-lora-rag.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    selected = {"english", "reserves", "revision", "china", "diversity", "pension", "modern", "false", "inject"}
    examples = [row["result"] for row in report["rows"] if row["case"]["id"] in selected]
    write_json(ROOT / "docs/chat_examples_v1.json", examples)
    text = """# Executed text-chat examples

These are actual outputs recorded by the `lora` backend with RAG on the
22-case diagnostic evaluation. They are not hand-written ideal answers.
Each turn is independent. The displayed text comes from `result.answer`;
the complete raw generation, retrieval IDs, status and latency are preserved
in [the JSON report](../reports/eval-lora-rag.json).

The `diversity` example contains an observed reversal of the supplied evidence;
it is included intentionally as a documented model failure. See the
[quality review](QUALITY_REVIEW.md). Do not treat these transcripts as ideal
answers or copy their historical claims without checking the notes.

**All replies are an educational historical simulation. They are not authentic
Lee Kuan Yew quotations.** A valid citation ID does not establish that every
claim is supported; read the cited source and the quality limitations.

To try text chat locally:

```bash
python -m lky.chat --backend lora
```

For a browser chat on a GPU:
[open the Colab notebook](https://colab.research.google.com/github/DiedrickD/99group-3/blob/main/notebooks/train_colab.ipynb),
run its cells, then use the temporary Gradio URL from its final cell.
This page is the permanent public chat-example link, not an always-on chatbot.

"""
    for index, result in enumerate(examples, 1):
        text += f"## Example {index}\n\n**User:** {result['question']}\n\n"
        text += f"**System status:** `{result['status']}`; warm latency {result['latency_seconds']:.3f}s.\n\n"
        text += render(result) + "\n\n"
    (ROOT / "docs/CHAT_EXAMPLES_V1.md").write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
