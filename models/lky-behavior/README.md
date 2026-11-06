---
base_model: Qwen/Qwen2.5-0.5B-Instruct
library_name: peft
license: apache-2.0
language:
- en
---

# Lee-inspired behavior LoRA: experimental v3

A separate rank-8 LoRA adapter for labelled hypothetical applications of
documented public decision patterns. It shares the pinned Qwen2.5-0.5B-Instruct
base with [the factual adapter](../lky-lora/README.md). This directory contains
adapter weights, not the base model.

The behavior adapter continued from the factual adapter: 24 authored examples
for three epochs, then 40 for one epoch (32 new plus eight replayed). There are
56 unique behavior examples across fourteen areas, with two source-held-out
validation examples. The two runs trained 540,672 parameters on a local CPU;
validation token loss changed from 2.1096 to 1.7529 to 1.6988. See
[stage 1](../../reports/training-behavior-stage1.json),
[stage 2](../../reports/training-behavior.json), and `run.json`.

Use `python app.py --backend lora` from the repository after installing its
requirements and downloading the base model. The runtime selects this adapter
for hypothetical/advice questions and the factual adapter for historical ones.
Historical precedents are rendered from RAG notes; model applications are
labelled interpretations. The architecture, full data provenance and reproduction
commands are in [BEHAVIOR.md](../../docs/BEHAVIOR.md).

This is an educational prototype, not an authentic speaker, a reproduction of
private thoughts, or a comprehensive model of Lee's beliefs. The small model can
give generic or off-topic advice and can make factual errors. Structure and
valid citation IDs do not establish fidelity; see
[actual failures](../../docs/QUALITY_REVIEW.md) and
[raw evaluation outputs](../../reports/behavior-lora-v3.json).

Distributed under Apache License 2.0. Base revision and artifact SHA-256 are
recorded in [the behavior manifest](../behavior_manifest.json). See
[MODEL_LICENSE.md](MODEL_LICENSE.md) and [NOTICE](../../NOTICE).
