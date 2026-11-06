# Recorded experiment results

Generated from the committed JSON reports. Small development diagnostics, not general historical accuracy scores.

Training completed on `cpu` with `Qwen/Qwen2.5-0.5B-Instruct`. The adapter trained 540,672 parameters for 2 epochs (14 optimizer steps) over 28 examples. Source-held-out validation token loss changed from 3.2400 to 2.4603. Training took 385.8 seconds. This does not establish an improvement in historical accuracy or persona quality.

| Configuration | Cases | Recall@3 | MRR@3 | Abstention recall | Raw reference validity | Fallbacks | Generated answers | Median seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [notes](../reports/eval-notes.json) | 22 | 1.000 | 1.000 | 1.000 | n/a | 0 | 0 | 0.000 |
| [base-rag](../reports/eval-base-rag.json) | 22 | 1.000 | 1.000 | 1.000 | 0.000 | 17 | 0 | 7.527 |
| [lora-rag](../reports/eval-lora-rag.json) | 22 | 1.000 | 1.000 | 1.000 | 0.941 | 1 | 16 | 6.272 |
| [base-no-rag](../reports/eval-base-no-rag.json) | 22 | 0.000 | 0.000 | 0.600 | 0.000 | 0 | 19 | 15.608 |
| [lora-no-rag](../reports/eval-lora-no-rag.json) | 22 | 0.000 | 0.000 | 0.600 | 0.000 | 0 | 19 | 5.291 |

The notes configuration is retrieval plus authored note summaries, without an LLM.
Citation validity checks only that cited note IDs were retrieved; it is not claim
entailment. The no-RAG configurations retain the evidence-only prompt, so their
retrieval scores are zero by design and their citation scores should not be
compared as if citations were available. Review raw output and structured
abstentions together: a model can verbally abstain without setting the
application's structured status. Latency excludes model initialization.

The first notes-only run had abstention recall 0.600 (3/5). The final run follows
development-time corrections; the original report is retained as
`eval-notes-initial.json`. A perfect score on the small corpus-specific diagnostic
set must not be described as 100% factual accuracy.

The Colab notebook is provided for reproduction. These records do not establish
a Colab execution or results for a larger model. Full transcripts are retained,
including failed raw citations and any fallback behavior.
