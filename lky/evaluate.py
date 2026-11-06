"""Local diagnostic eval: retrieval, abstention, citation references and latency.

Citation validity checks IDs, not semantic entailment. Raw generations are kept
so the fallback cannot conceal a model's failed citation behavior.
"""
import argparse
import math
import re
import statistics
from .chat import Chatbot
from .data import ROOT, read_jsonl, write_json, digest


def ratio(n, d):
    return n / d if d else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["notes", "base", "lora"], default="notes")
    parser.add_argument("--no-rag", action="store_true")
    parser.add_argument("--ids", help="Comma-separated subset; the selected IDs are recorded")
    parser.add_argument("--output", default="reports/eval-notes.json")
    args = parser.parse_args()
    cases = read_jsonl(ROOT / "data/eval.jsonl")
    if args.ids:
        selected = set(args.ids.split(","))
        missing = selected - {r["id"] for r in cases}
        if missing:
            parser.error(f"Unknown evaluation IDs: {sorted(missing)}")
        cases = [row for row in cases if row["id"] in selected]
    bot = Chatbot(backend=args.backend, use_rag=not args.no_rag)
    rows, recall, rr, held_out = [], [], [], []
    for case in cases:
        result = bot.answer(case["question"])
        gold = set(case["relevant_note_ids"])
        retrieved = result["retrieved"]
        recall_value = len(gold & set(retrieved)) / len(gold) if gold else None
        reciprocal_rank = next((1 / (i+1) for i, nid in enumerate(retrieved) if nid in gold), 0.0) if gold else None
        if gold:
            recall.append(recall_value)
            rr.append(reciprocal_rank)
            if not case["training_source_overlap"]:
                held_out.append(recall_value)
        cited = set(re.findall(r"\[(N\d+)\]", result["answer"]))
        raw_cited = set(re.findall(r"\[(N\d+)\]", result["raw_generation"]))
        row = {"case": case, "result": result, "recall_at_3": recall_value,
               "reciprocal_rank_at_3": reciprocal_rank,
               "citation_ids_valid": bool(cited) and cited <= set(retrieved),
               "raw_citation_ids_valid": bool(raw_cited) and raw_cited <= set(retrieved),
               "expected_abstention_matched": (result["status"] == "abstained") == case["expected_abstain"]}
        rows.append(row)
        print(f'{case["id"]}: {result["status"]}; retrieved={retrieved}', flush=True)
    tp = sum(r["case"]["expected_abstain"] and r["result"]["status"] == "abstained" for r in rows)
    fp = sum(not r["case"]["expected_abstain"] and r["result"]["status"] == "abstained" for r in rows)
    fn = sum(r["case"]["expected_abstain"] and r["result"]["status"] != "abstained" for r in rows)
    answered = [r for r in rows if r["result"]["status"] != "abstained"]
    raw = [r for r in rows if r["result"]["raw_generation"]]
    latencies = sorted(r["result"]["latency_seconds"] for r in rows)
    metrics = {"recall_at_3": statistics.mean(recall) if recall else None,
               "mrr_at_3": statistics.mean(rr) if rr else None,
               "training_source_held_out_recall_at_3": statistics.mean(held_out) if held_out else None,
               "abstention_precision": ratio(tp, tp + fp), "abstention_recall": ratio(tp, tp + fn),
               "false_abstentions": fp, "missed_abstentions": fn,
               "final_reference_validity_rate": ratio(sum(r["citation_ids_valid"] for r in answered), len(answered)),
               "raw_generation_reference_validity_rate": ratio(sum(r["raw_citation_ids_valid"] for r in raw), len(raw)),
               "citation_fallback_count": sum(r["result"]["citation_fallback"] for r in rows),
               "generated_answer_count": sum(r["result"]["status"] == "generated" for r in rows),
               "notes_answer_count": sum(r["result"]["status"] in {"source_notes", "notes_fallback"} for r in rows),
               "latency_median_seconds": statistics.median(latencies),
               "latency_p95_seconds": latencies[max(0, math.ceil(len(latencies)*0.95)-1)]}
    report = {"backend": args.backend, "rag": not args.no_rag, "cases": len(rows),
              "selected_ids": [r["case"]["id"] for r in rows],
              "eval_data_sha256": digest(ROOT / "data/eval.jsonl"),
              "notes_sha256": digest(ROOT / "data/notes.jsonl"), "metrics": metrics, "rows": rows,
              "limitations": ["Small authored diagnostic benchmark; questions reflect the starter corpus.",
                              "Source-held-out means absent from fine-tuning, present in retrieval; it does not imply an independent benchmark.",
                              "Citation validity is referential integrity, not factual entailment or faithfulness.",
                              "Lexical abstention and injection patterns are incomplete; adversarial robustness is not established.",
                              "Latency excludes model loading; deterministic decoding is used.",
                              "No-RAG ablation retains the evidence-only instruction; it measures missing evidence under this policy."]}
    write_json(ROOT / args.output, report)
    print(metrics)


if __name__ == "__main__":
    main()
