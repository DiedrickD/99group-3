# Evaluation and its limits

The measured JSON reports in `reports/` are the source of truth. The generated
`RESULTS.md` presents their comparison. Results are from a tiny **development
diagnostic benchmark**, not a historical accuracy certification.

[The qualitative review](QUALITY_REVIEW.md) records an actual comparison reversal
despite a valid citation, an unsupported expansion and a repeated-output failure.

## Metrics

| Metric | Definition | What it does not prove |
| --- | --- | --- |
| Recall@3 | Fraction of labelled relevant notes found among the first three retrieved notes, averaged over answerable questions | Coverage of history or robust semantic retrieval |
| MRR@3 | Mean reciprocal rank of the first labelled relevant note, zero if absent | Faithfulness of the generated answer |
| Training-source-held-out Recall@3 | Recall for S07/S08 notes absent from fine-tuning | An independent, blind test of generalization |
| Abstention precision | Correctly abstained cases divided by all structured abstentions | Reliable refusal under every unseen phrasing |
| Abstention recall | Correctly abstained cases divided by labelled unsupported/policy cases | No unsupported claims in otherwise answered cases |
| Final reference validity | Answered cases with nonempty citation IDs wholly inside the retrieved set | Citation entailment or factual correctness |
| Raw reference validity | The same ID check on pre-fallback generations | Overall faithfulness |
| Citation fallback count | How many generated answers needed replacement by source-note summaries | LLM answer success |
| Median / p95 latency | Warm answer latency, including retrieval and generation, excluding model loading | Cold-start or multi-user service performance |

Reference validity is calculated per answer, not per claim. Abstention metrics
use the application's structured status, so semantic abstentions written by a
model must also be inspected manually. The benchmark has seventeen answerable
cases and five expected abstentions.

## A concrete benefit from evaluation

The first notes-backend run found all labelled relevant notes, but abstained on
only three of five expected abstentions. A possessive suffix was indexed as a
word, and generic speech-related terms also matched irrelevant material.
`eval-notes-initial.json` preserves that result.

The tokenization correction removes possessive fragments and generic speech
terms. An attribution check handles requests assigning post-2015 speeches to
Lee while allowing explicitly hypothetical modern questions. The final
notes-backend report records the rerun. Because these fixes used the diagnostic
questions, the final score is development evidence, not an untouched test result.

## Compare five configurations

1. Notes only: retrieval plus a labelled summary; no LLM.
2. Base model with RAG.
3. LoRA adapter with RAG.
4. Base model without RAG.
5. LoRA adapter without RAG.

The same prompt policy, question set and deterministic decoding are used where
applicable. The no-RAG ablation retains the evidence-only policy. It is expected
to have poor supported-answer coverage when the evidence is removed. Do not
interpret that as an unrestricted test of pretrained knowledge.

## Human review required for stronger claims

Inspect raw generations, final answers and primary passages together. Rate each
dimension from 1 (poor) to 5 (strong):

- **Historical support:** each factual claim follows from the source and respects its date.
- **Attribution:** documented views are separated from the system's reconstruction.
- **Useful uncertainty:** absence of evidence, disputed interpretations and gaps are explicit.
- **Style:** concise, direct and pragmatic without inventing personal memories.
- **Usefulness:** answers the actual question and explains relevant constraints.

Add counterexamples: personal biography absent from the index, paraphrases with
no shared vocabulary, multilingual queries, conflicting statements from different
decades, adversarial instructions and invented quotations. An independent
historian-reviewed set and blinded base-versus-adapter comparison would be a
substantial improvement over this starter.

No RAGAS, DeepEval or external LLM judge scores are claimed. Automated citation
checks and small source-held-out loss measurements cannot substitute for that
review.
