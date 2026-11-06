import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    names = ["notes", "base-rag", "lora-rag", "base-no-rag", "lora-no-rag"]
    text = "# Recorded experiment results\n\nGenerated from the committed JSON reports. Small development diagnostics, not general historical accuracy scores.\n\n"
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
    (ROOT / "docs/RESULTS.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
