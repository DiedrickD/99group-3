import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    names = ["notes", "base-rag", "lora-rag", "base-no-rag", "lora-no-rag"]
    text = "# Recorded experiment results\n\nGenerated from the committed JSON reports. Small development diagnostics, not general historical accuracy scores.\n\n## Original factual experiment (v1 strict-evidence runtime)\n\nThese original reports predate the behavior adapter and current hypothetical routing. Their historical abstention policy is not the current policy.\n\n"
    training = json.loads((ROOT / "reports/training.json").read_text(encoding="utf-8"))
    text += (f"Training completed on `{training['device']}` with `{training['base_model']['model_id']}`. "
             f"The adapter trained {training['trainable_parameters']:,} parameters for {training['epochs']} epochs "
             f"({training['optimizer_steps']} optimizer steps) over {training['train_examples']} examples. "
             f"Source-held-out validation token loss changed from {training['validation_loss_before']:.4f} "
             f"to {training['validation_loss_after']:.4f}. Training took {training['elapsed_seconds']:.1f} seconds. "
             "This does not establish an improvement in historical accuracy or persona quality.\n\n")
    text += "| Configuration | Cases | Recall@3 | MRR@3 | Abstention recall | Raw reference validity | Fallbacks | Generated answers | Median seconds |\n"
    text += "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n"
    def fmt(value):
        return "n/a" if value is None else f"{value:.3f}"
    reports = []
    for name in names:
        path = ROOT / f"reports/eval-{name}.json"
        if not path.exists():
            continue
        report = json.loads(path.read_text(encoding="utf-8"))
        reports.append(report)
        m = report["metrics"]
        text += (f"| [{name}](../reports/eval-{name}.json) | {report['cases']} | {fmt(m['recall_at_3'])} | "
                 f"{fmt(m['mrr_at_3'])} | {fmt(m['abstention_recall'])} | {fmt(m['raw_generation_reference_validity_rate'])} | "
                 f"{m['citation_fallback_count']} | {m['generated_answer_count']} | {fmt(m['latency_median_seconds'])} |\n")
    text += """
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
"""
    if (ROOT / "reports/behavior-lora-v3.json").exists():
        current = json.loads((ROOT / "reports/behavior-lora-v3.json").read_text(encoding="utf-8"))
        baseline = json.loads((ROOT / "reports/behavior-baseline-v3.json").read_text(encoding="utf-8"))
        metrics = current["metrics"]
        subset = [row for row in current["rows"] if row["case"]["id"] in baseline["selected_ids"]]
        structured = sum(row["three_parts_present"] for row in subset)
        text += f"""
## Current behavior experiment (v3)

The separate behavior adapter continued from the factual adapter: 24 examples
for three epochs, then 40 examples for one epoch (32 new plus eight replayed).
That is 56 unique authored behavior examples across 14 areas, with two validation
examples. A separate intent router was trained on 48 labelled questions.

- Routing/correction/label checks: {metrics['routing_and_labels_passed']}/{current['cases']}.
- Hypothetical LLM answers: {metrics['hypothetical_model_answers']}.
- Raw three-part answers: {metrics['three_part_model_answers']}/{metrics['hypothetical_model_answers']}.
- Labelled analogous precedents retrieved: {metrics['labelled_precedents_found']}/{metrics['labelled_precedent_cases']}.
- Same four development cases, same prompt and evidence: the original adapter
  produced {baseline['metrics']['three_part_model_answers']}/4 three-part answers;
  the behavior adapter produced {structured}/4. This is a format comparison,
  not a persona-fidelity or recommendation-quality score.

[Current raw outputs](../reports/behavior-lora-v3.json),
[original-adapter comparison](../reports/behavior-baseline-v3.json),
[notes-only check](../reports/behavior-notes-v3.json).

Manual inspection found a reversed causal phrase in a generated historical
precedent and several generic or off-topic applications. The current interface
therefore renders factual precedents from source notes and extracts the model's
application separately. The report records this display transformation and
retains the raw output and original metrics. It is not a new generation run.
See [quality review](QUALITY_REVIEW.md) and [training details](BEHAVIOR.md).

These were announced development cases, including the user's earthquake example.
They are not an independent blind test. There is no measured score for reproducing
Lee's actual decisions, private thinking, or all domains of his life.
"""
    (ROOT / "docs/RESULTS.md").write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
