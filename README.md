# What Would Lee Kuan Yew Do?

A text chatbot trained to apply selected, documented public decision patterns
of Lee Kuan Yew to new situations. Historical evidence and hypothetical
recommendations are visibly distinguished. This is an educational simulation,
not Lee himself, a complete model of his beliefs, or a transcript of private thought.

[Chat examples](docs/CHAT_EXAMPLES.md) | [Behavior and architecture](docs/BEHAVIOR.md) |
[Submission text](docs/SUBMISSION.md) | [Sources](docs/DATASET.md) |
[Results](docs/RESULTS.md) | [Evaluation](docs/EVALUATION.md) |
[Colab notebook](https://colab.research.google.com/github/DiedrickD/99group-3/blob/main/notebooks/train_colab.ipynb)

The live demonstration URL and availability are recorded in [DEMO.md](docs/DEMO.md).
The deliverable folder is `99task_lee_kuan_yew_llm`; its contents are the repository
root. Internal research remains outside Git.

## How it answers

- **Historical question:** retrieve evidence and answer with the factual adapter.
- **New scenario or advice:** retrieve analogous cases, then use the behavior
  adapter to explain a precedent, a possible application and the limits of the analogy.
- **False historical premise:** correct it, then address the underlying hypothetical.

For example, a question about a large earthquake can retrieve the documented
Bukit Ho Swee urban-fire rehousing response. The model may apply coordination
and recovery principles, while explaining that a fire and an earthquake require
different technical responses. It must not invent a forest-fire policy or claim
that Lee made the new recommendation.

## Three trained roles

1. A small multinomial Naive Bayes intent router trained on 48 labelled questions,
   with explicit routing rules for clear requests and false premises.
2. A factual LoRA adapter trained on 28 authored source-grounded examples.
3. A separate behavior LoRA adapter trained in two stages using 56 unique
   event/action/application examples, including replay of eight earlier examples.

The two adapters share a pinned Apache-2.0 Qwen2.5-0.5B-Instruct base model.
This avoids loading three independent large language models. Actual local
training reports, parent hashes and data hashes are committed.

The behavior extension covers fourteen areas: disaster recovery, economic
shocks, fiscal resilience, leadership, succession, integrity and merit, labour
negotiation, shared growth, education, technological change, foreign policy,
talent and innovation, language policy, and social cohesion. These are selected
public decision patterns, not exhaustive coverage of his life and beliefs.
The [coverage map and research gaps](docs/RESEARCH_COVERAGE.md) explain which
themes have evidence and how to expand beyond the present small corpus.

## Data and evidence

Ten source records support 21 short original research notes: nine primary
speeches and one NLB historical article. No complete speeches or memoirs are
redistributed. The original factual dataset and results remain preserved, while
separate `behavior_*`, `extended_*` and router files record the extension.

The NTUC speech's discussion of training workers for computer adoption is a
useful precedent for a hypothetical AI response. It does not establish Lee's
actual opinion of ChatGPT. Sources for analogous principles support the
historical basis rather than proving the new conclusion.

## Run

Python 3.12 is the tested version. Retrieve notes without model dependencies:

```bash
git clone https://github.com/DiedrickD/99group-3.git 99task_lee_kuan_yew_llm
cd 99task_lee_kuan_yew_llm
python -m lky.chat --question "What would Lee do about a severe crisis?"
```

The dependency-free CLI defaults to `notes`, with an explicitly labelled authored
outline for hypotheticals. The browser app defaults to the trained LLM. Install
dependencies and select `lora` explicitly for a trained command-line response:

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-demo.txt
python -m lky.chat --backend lora --question "What would Lee do about a severe crisis?"
python app.py --backend lora
# Temporary public link:
python app.py --backend lora --share
```

The first model call downloads approximately 1 GB of base weights to ignored
storage. Each turn is independent; the app does not persist conversations.
`requirements-lock-windows.txt` records the tested local environment. Use
`requirements-colab.txt` to preserve Colab's CUDA-enabled PyTorch.

## Train and evaluate

[BEHAVIOR.md](docs/BEHAVIOR.md) contains the exact two-stage training workflow.
The Colab notebook reproduces the factual adapter, router and behavior adapter.
A supplied notebook is not a claim that a GPU run has been completed.

```bash
python scripts/validate_data.py
python scripts/validate_behavior.py
python -m unittest discover -s tests -v
python -m lky.evaluate_persona --backend lora --output reports/local-behavior.json
```

RAG currently combines BM25 with curated topic metadata. It can retrieve an
analogy without an exact topic match, but it is not universal semantic retrieval.
Evaluation checks routing, analogue retrieval, corrections, response structure
and raw generations. Human review is needed for faithfulness, useful transfer,
tradeoffs and historical fidelity. A 0.5B model and this small synthetic dataset
can still make factual and reasoning errors.

The original 22-case results describe the earlier strict-evidence runtime;
the new behavior diagnostics are separate. See [results](docs/RESULTS.md) and
[quality review](docs/QUALITY_REVIEW.md). GitHub-hosted checks were unable to
start because of an account restriction; local checks are recorded separately.

Code: [MIT](LICENSE). Original project data: [CC BY 4.0](DATA_LICENSE.md).
Adapters: Apache-2.0. Third-party source and base-model rights remain separate;
see [NOTICE](NOTICE).
