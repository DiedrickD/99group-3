# What Would Lee Kuan Yew Do?

A text-only, source-grounded **historical simulation** with an open-weight model,
LoRA training, retrieval-augmented generation (RAG), and diagnostic evaluation.
Replies are generated reconstructions, never authentic Lee Kuan Yew quotations.

[Chat examples](docs/CHAT_EXAMPLES.md) · [Submission text](docs/SUBMISSION.md) ·
[Dataset and sources](docs/DATASET.md) · [Workflow](docs/WORKFLOW.md) ·
[Evaluation](docs/EVALUATION.md) ·
[Open training notebook in Colab](https://colab.research.google.com/github/DiedrickD/99group-3/blob/main/notebooks/train_colab.ipynb)

[Temporary live trained-model chat](https://3baba5f3e0cf4f2513.gradio.live)
([availability and verification](docs/DEMO.md)).

The local deliverable folder is named `99task_lee_kuan_yew_llm`; its contents are
the root of this repository. Internal research is maintained separately and is
not pushed.

## What this project contains

- Eight official speech source records from PMO, MFA and NAS, covering 1965-2011.
- Sixteen original, source-linked research notes; no full speech or memoir text.
- Twenty-eight authored training examples and four source-held-out validation
  examples. Two questions per training note reuse one authored answer.
- Qwen2.5-0.5B-Instruct, an Apache-2.0 open-weight base model, with a small LoRA
  experiment. Exact model revision and run details are recorded in `config/`
  and `reports/`. This is a feasibility prototype, not a historically validated
  or production-quality persona model.
- BM25 retrieval, source references, an insufficient-evidence response, modern
  extrapolation labels and a citation-ID fallback.
- A 22-question diagnostic benchmark, raw model outputs, deterministic checks,
  CLI chat and an optional Gradio interface.

See [the evaluation report](docs/EVALUATION.md) for the actual measured results
and [the model card](docs/MODEL_CARD.md) for limits. The Colab notebook is a
reproducible workflow template; a successful local run does not imply that a
Colab run or a larger-model experiment has been completed.

The [quality review](docs/QUALITY_REVIEW.md) records observed factual and style
errors, including a claim that reverses the supplied evidence despite citing a
valid note. The trained adapter is experimental; the default notes backend is
provided for transparent evidence lookup.

## Run without model dependencies

Python 3.12 is the tested version. The explicit `notes` backend retrieves and
summarises the authored notes; it does **not** invoke a language model.

```bash
git clone https://github.com/DiedrickD/99group-3.git 99task_lee_kuan_yew_llm
cd 99task_lee_kuan_yew_llm
python -m lky.chat --question "Why maintain national reserves?"
python scripts/validate_data.py
python -m unittest discover -s tests -v
python -m lky.evaluate --output reports/local-notes.json
```

## Run the language model or train the adapter

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m lky.chat --backend base --question "Why maintain national reserves?"
python -m lky.chat --backend lora --question "Why maintain national reserves?"

# Reproduce training using the exact revision already in config/model.json:
python -m lky.train --epochs 2
```

The first model call downloads roughly 1 GB of base weights to ignored local
storage. CPU inference uses float32; CUDA uses float16. Model weights remain
separate from the small published adapter. To deliberately resolve a new model
revision, run `python scripts/prepare_model.py` and record the changed config.
`requirements-lock-windows.txt` records the tested Windows environment; use
`requirements-colab.txt` in Colab to preserve its CUDA-enabled PyTorch.

For a GPU experiment, use the Colab link above. The notebook preserves Colab's
CUDA-enabled PyTorch, supports the 0.5B model or a deliberate 1.5B upgrade,
downloads run artifacts, and can create a temporary chat share URL.

## Optional text chat interface

```bash
python -m pip install -r requirements-demo.txt
python app.py --backend lora
# Temporary public link, tied to the lifetime of this process:
python app.py --backend lora --share
```

Use the printed URL. Each turn is independent; history is shown for reading and
is not passed to the model. The application does not persist chat messages.
A Gradio share link is temporary; the GitHub chat examples are the permanent
review link. No always-on hosting service is claimed.

## Why both fine-tuning and RAG?

Fine-tuning adjusts how the model responds: direct wording, pragmatic framing,
source markers and uncertainty. RAG supplies what it can support: dated notes
with traceable sources. Evaluation tests each part, exposes regressions and
checks whether added complexity helps. These functions are complementary;
fine-tuning alone cannot make historical attribution reliable.

The starter uses BM25 rather than embeddings because its index has only sixteen
short English notes. Dense retrieval, reranking, a vector database and RAGAS are
documented expansion options, not implemented features.

## Scope and rights

The starter focuses on documented public-policy themes. It cannot answer every
question about Lee's life, private memories or current events. Modern applications
must be labelled as extrapolations. Lexical filtering and valid citation IDs do
not guarantee factual correctness or resistance to prompt injection.

Memoirs including *The Singapore Story* and *From Third World to First* are
identified for a future permissioned expansion; **their full texts were not used
in this run**. Public access to a speech is not treated as an open license.
[Data provenance and rights](docs/DATASET.md) explain the distinction.

Code: [MIT](LICENSE). Original project notes and authored QA:
[CC BY 4.0](DATA_LICENSE.md). Base-model and third-party source rights remain
separate; see [NOTICE](NOTICE).
