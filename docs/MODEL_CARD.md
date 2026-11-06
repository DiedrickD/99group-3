# Model card: source-grounded Lee Kuan Yew simulation adapter

## Current model package

The package now includes a trained intent classifier and two LoRA variants that
share the same base model. The original factual adapter described below is
preserved. The separate behavior adapter learned Precedent/Application/Limit
answers from 56 unique authored analogies across fourteen domains; its exact
two-stage runs are in `reports/training-behavior-stage1.json` and
`reports/training-behavior.json`. See [BEHAVIOR.md](BEHAVIOR.md). The new model
can answer hypothetical scenarios without an exact matching historical speech;
it still cannot recover private thoughts or establish a modern opinion of Lee.

## Model and intended use

Base: [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct).
Exact revision: `7ae557604adf67be50417f59c2c2f167def9a775`.
The model card identifies the base as Apache-2.0; the small adapter is also
distributed under Apache-2.0. Base weights are downloaded separately.

Intended use: an educational text demonstration of source-grounded historical
reconstruction. It is not an authentic speaker, a biographical authority, an
official government service or a reliable account of what Lee would think today.
The disclosed persona can use first-person phrasing; that does not turn its
answers into quotations or first-person historical evidence.

## Original factual training run

Training completed locally on **6 November 2026**, using Windows, Python 3.12,
PyTorch 2.6.0 CPU and an Intel i5-1135G7 host. The run used 28 authored training
examples and four validation examples from a source excluded from training.
Only short original notes and original answers were used; no full memoir text
or full speech collection was ingested.

| Setting | Recorded value |
| --- | --- |
| Method | LoRA supervised causal language modelling |
| Trainable parameters | 540,672 |
| Total parameters including adapter | 494,573,440 |
| Targets | `q_proj`, `v_proj` |
| Rank / alpha / dropout | 8 / 16 / 0.05 |
| Epochs / optimizer steps | 2 / 14 |
| Learning rate | 0.0002 |
| Micro-batch / accumulation | 1 / 4 |
| Maximum sequence length | 384 tokens |
| Loss labels | Assistant answer tokens only |
| Seed | 42 |
| Validation token loss before / after | 3.23995 / 2.46032 |
| Timed training and validation loop | 385.79 seconds |

The exact run report, hashes and per-epoch losses are in
[`reports/training.json`](../reports/training.json). Downloading and loading the
base model are excluded from the timed loop. Lower validation loss on four
examples is not evidence of general factual accuracy or better persona quality.

## Runtime behavior

The current browser app defaults to `lora` and switches between the factual and
behavior adapters according to question intent. Hypothetical answers receive
analogous cases and a separate behavior prompt. The interface renders factual
precedents from source notes and extracts the model's generated application;
raw output is retained for evaluation. Unsupported historical questions can
abstain, while explicitly hypothetical questions can answer without a document.

RAG supplies up to three authored research notes. Deterministic decoding uses
at most 180 new tokens. The prompt asks for a concise, direct reconstruction
with note citations. Simple policy checks precede retrieval. Missing or invalid
note citations in historical answers trigger a labelled note-summary fallback; raw generations are
retained in evaluation reports.

The CLI's default `notes` backend is a separate non-LLM mode, with authored
outlines for hypotheticals. A response from that
backend or a citation fallback must not be counted as a successfully generated
answer from the adapter. Modern extrapolation labels do not verify modern facts.

## Known limitations

- A 0.5B model, 28 factual examples and 56 unique behavior examples provide limited language and reasoning quality.
- Training answers and diagnostic questions were AI-assisted; there is no
  independent historian review or blinded style comparison.
- Two questions per note reuse an answer, limiting training diversity.
- Source coverage is narrow, selective and weighted toward public policy.
- Official primary speeches express a participant's position, not a complete
  or neutral historical record. The corpus does not settle disputed history.
- BM25 can fail on synonyms, ambiguous terms and multilingual questions.
- A model can invent or distort a claim while citing a valid note ID.
- Lexical input and attribution checks do not establish comprehensive
  resistance to prompt injection or fabricated quotations.
- The current interface treats turns independently and does not resolve follow-up
  pronouns or preserve a conversation's context.
- The adapter cannot establish the deceased speaker's opinion about new events.

## Reproduction and alternatives

Follow the README or the Colab notebook. Preserve the committed model revision
for reproduction; `scripts/prepare_model.py` deliberately resolves a revision
and can change that configuration. The optional 1.5B model requires a separate
training and evaluation run. No results for that model or a Colab runtime are
claimed by this local run's artifacts.
