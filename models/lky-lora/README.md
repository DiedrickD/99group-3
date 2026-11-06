---
base_model: Qwen/Qwen2.5-0.5B-Instruct
library_name: peft
license: apache-2.0
language: en
---

# Lee Kuan Yew historical-simulation LoRA adapter

A small, locally trained feasibility experiment for source-grounded educational
text reconstruction. Generated responses are not authentic quotations.

See the [complete model card](../../docs/MODEL_CARD.md),
[training report](../../reports/training.json), and
[source register](../../docs/DATASET.md).

Base revision: `7ae557604adf67be50417f59c2c2f167def9a775`.
Trainable parameters: 540,672. Two epochs on 28 authored examples, with four
source-held-out validation examples. No full memoir text was used.

The adapter requires the base model and its unchanged tokenizer, downloaded
separately by the application. See `MODEL_LICENSE.md` for licensing.
