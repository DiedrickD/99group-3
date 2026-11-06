# Ready-to-paste challenge response

## Lee Kuan Yew Chatbot Implementation

I built “What Would Lee Kuan Yew Do?”, a text-based educational chatbot that
reconstructs a concise, pragmatic response using documented historical evidence.
Every reply identifies itself as a simulation; generated first-person wording
is not presented as an authentic quotation.

The implementation combines an Apache-2.0 open-weight model,
Qwen2.5-0.5B-Instruct, with a trained LoRA adapter and retrieval-augmented
generation (RAG). I completed a small local fine-tuning run on 28 authored
examples for two epochs. The adapter updates 540,672 parameters. Four examples
from a separate source provide validation loss measurements. This is a
feasibility prototype, rather than a production-quality reconstruction of Lee.

The starter knowledge base contains 16 original research notes linked to eight
official speeches from Singapore's Prime Minister's Office, Ministry of Foreign
Affairs and National Archives. Topics include bilingualism, education, national
reserves, pragmatic policy changes, water constraints, US-China relations,
small-state security and leadership integrity. The source register records event
dates and passage locators, including a webpage whose displayed publication
date differs from the speech's event date.

At question time, BM25 retrieves relevant notes. The model uses those notes to
answer with source references. Unsupported questions receive an insufficient-
evidence response. Applications to modern events are labelled as extrapolations.
Invalid or missing note citations trigger a clearly identified source-note
fallback, while the original generation is retained for evaluation.

Executed chat examples, training metadata, evaluation reports, setup instructions
and a Colab GPU workflow are public in the repository. The project includes CLI
chat and an optional Gradio text interface. A Gradio share URL is temporary;
the GitHub examples provide the permanent review link.

The public dataset contains original short paraphrases and authored answers,
not full speech transcripts or books. Relevant memoirs, including The Singapore
Story and From Third World to First, are documented as future permissioned
sources; their full texts were not used in this run. Coverage of personal life
and arbitrary topics remains limited by the starter corpus.

## Repository / Workflow Links

- Public repository: https://github.com/DiedrickD/99group-3
- Executed chat examples: https://github.com/DiedrickD/99group-3/blob/main/docs/CHAT_EXAMPLES.md
- Dataset and source list: https://github.com/DiedrickD/99group-3/blob/main/docs/DATASET.md
- Workflow: https://github.com/DiedrickD/99group-3/blob/main/docs/WORKFLOW.md
- Recorded results: https://github.com/DiedrickD/99group-3/blob/main/docs/RESULTS.md
- Colab notebook: https://colab.research.google.com/github/DiedrickD/99group-3/blob/main/notebooks/train_colab.ipynb

## Technical Approach & Implementation Notes

**Research and dataset.** I selected primary speeches, checked speaker identity
and event dates, and wrote short source-linked notes and supervised QA. Splits
are grouped by source: six speeches supply training data, one supplies validation
data, and another is excluded from both. All notes remain retrievable, including
sources absent from fine-tuning. The data manifest includes hashes and provenance.
The examples are AI-assisted and have not undergone independent historian review.

**Model training.** PyTorch, Hugging Face Transformers and PEFT train a rank-8
LoRA adapter over attention query/value projections. Only assistant tokens
contribute to training loss. The exact model commit, seed, settings, data hashes
and losses are recorded. Source-held-out validation token loss changed from
3.240 to 2.460 after two epochs; that result does not establish historical
accuracy or an improvement in user-facing answer quality.

**RAG.** The small index uses BM25 rather than a vector database or embeddings.
RAG supplies inspectable, dated evidence and enables updates without retraining.
It also lets the model use sources excluded from its supervised training. Source
links support verification, but valid citation IDs alone cannot establish that
every claim is entailed by its evidence.

**Evaluation.** I use 22 diagnostic questions spanning historical questions,
modern extrapolation, insufficient evidence, false attribution and instruction
override attempts. Reports include Recall@3, MRR@3, abstention precision/recall,
raw and final citation-ID validity, fallback counts and warm latency. The base
model and adapter are compared with and without retrieval. Raw outputs are
retained so fallback summaries cannot inflate model-generation success. The
adapter produced valid note IDs on 16 of 17 answerable RAG cases, compared with
0 of 17 for the base model; this measures citation formatting, not claim support.
The final RAG diagnostic Recall@3 and MRR@3 were both 1.0 on the small,
corpus-specific question set. The
initial notes-only evaluation exposed two unsupported answers; its result is
preserved alongside the corrected run. These are development diagnostics,
not an independent test or a claim of 100% factual accuracy. Human assessment
of claim support, attribution, uncertainty, style and usefulness remains necessary.
Inspection found a generated comparison that reversed the evidence despite a
valid citation, so the adapter remains experimental and the evidence-note mode
is the default. The quality review preserves that failure explicitly.

**Tools and workflow.** Python handles source metadata, JSONL data, BM25 and
metrics; PyTorch/Transformers/PEFT handle model training and inference;
safetensors stores the adapter; Gradio provides optional text chat; GitHub
Actions checks data and grounding behavior. The Colab notebook is provided for
GPU reproduction and an optional larger-model experiment; no Colab or larger-
model execution is claimed by the local run. Flowise, a vector database and an
external LLM judge are not required for this starter.
