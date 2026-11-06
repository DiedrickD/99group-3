# Workflow

Research -> source records -> event/action cases -> authored analogies ->
source-separated training -> routing and case retrieval -> model response -> evaluation.

The detailed architecture, exact commands and examples are in
[BEHAVIOR.md](BEHAVIOR.md).

1. Research primary speeches and reliable institutional histories across domains.
   Record dates, speaker identity, passage locators and rights. Do not infer a
   personal action from an entire government's response without qualification.
2. Keep observed behavior separate from inferred principles and imagined
   applications. Each case includes a transfer limit.
3. Train a small intent router, preserve the factual adapter, and train a separate
   behavior adapter on Precedent/Application/Limit targets. The adapters share a base.
4. Retrieve historical evidence for historical questions and analogous cases for
   new scenarios. A missing exact document must not automatically block an
   explicitly hypothetical answer.
5. Correct false premises, answer the underlying hypothetical and identify the
   historical sources as support for principles rather than proof of modern views.
6. Evaluate unseen response scenarios, routing, precedent selection, source
   attribution, structure and useful uncertainty. Keep raw outputs and distinguish
   the original strict-evidence experiment from the behavior extension.

RAG supplies inspectable precedents. Fine-tuning learns how to connect those
precedents to a new recommendation. Evaluation checks whether the analogy
is relevant, the factual account is faithful and the inferred recommendation
is distinguished from Lee's documented words.

Tools used: Python, a standard-library Naive Bayes router, PyTorch,
Transformers, PEFT, safetensors, BM25, curated topic metadata, Gradio, Git and
GitHub Actions. Context7 supplied library documentation. Colab is provided
as a GPU reproduction workflow. No external LLM judge, vector database,
Flowise or RAGAS score is claimed.
