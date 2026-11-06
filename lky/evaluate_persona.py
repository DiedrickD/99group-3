"""Evaluate v3 factual-versus-hypothetical behavior without relabelling legacy results."""
import argparse
import re
from .chat import Chatbot
from .data import ROOT, digest, read_jsonl, write_json
from .retrieval import Retriever


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["notes", "base", "lora"], default="notes")
    parser.add_argument("--output", default="reports/behavior-notes-v3.json")
    parser.add_argument("--original-adapter", action="store_true")
    parser.add_argument("--ids")
    args = parser.parse_args()
    bot = Chatbot(args.backend, enable_behavior=not args.original_adapter)
    cases = read_jsonl(ROOT / "data/persona_eval.jsonl")
    if args.ids:
        ids = set(args.ids.split(","))
        if ids - {c["id"] for c in cases}:
            parser.error("Unknown case ID")
        cases = [c for c in cases if c["id"] in ids]
    rows = []
    for case in cases:
        retriever = bot.retriever
        if case.get("empty_corpus"):
            bot.retriever = Retriever([])
        result = bot.answer(case["question"])
        bot.retriever = retriever
        checks = {
            "mode_matches": result["response_mode"] == case["expected_mode"],
            "abstention_matches": (result["status"] == "abstained") == case["expected_abstain"],
            "correction_matches": bool(result["premise_correction"]) == case["expected_correction"],
            "interpretation_label_present": case["expected_mode"] != "hypothetical" or case["expected_abstain"] or "Hypothetical interpretation" in result["answer"],
        }
        raw = result["raw_generation"]
        refusal = bool(re.search(r"cannot (answer|provide)|insufficient evidence|not enough (evidence|information)|no information", raw, re.IGNORECASE))
        fabricated_speech = bool(re.search(r"\bin 2024\b.{0,45}\b(I|Lee|he) (gave|delivered)|\b(I|Lee|he) (gave|delivered)\b.{0,45}\bin 2024\b", raw, re.IGNORECASE))
        cited = set(re.findall(r"\[([NC]\d+)\]", raw))
        rows.append({"case": case, "result": result, "checks": checks,
                     "three_parts_present": all(part.lower() in raw.lower() for part in ["Precedent:", "Application:", "Limit:"]),
                     "raw_precedent_ids_valid": bool(cited) and cited <= set(result["retrieved"]),
                     "labelled_precedent_retrieved": case.get("relevant_precedent") in result["retrieved"] if case.get("relevant_precedent") else None,
                     "raw_refusal_pattern": refusal, "raw_speech_fabrication_pattern": fabricated_speech})
        print(f'{case["id"]}: {result["status"]}; checks={all(checks.values())}; raw_refusal={refusal}', flush=True)
    report = {"runtime_policy": "v3", "backend": args.backend, "cases": len(rows),
              "selected_ids": [c["id"] for c in cases], "behavior_adapter_enabled": not args.original_adapter,
              "dataset_sha256": digest(ROOT / "data/persona_eval.jsonl"),
              "persona_sha256": digest(ROOT / "data/persona.json"),
              "behavior_adapter_sha256": digest(ROOT / "models/lky-behavior/adapter_model.safetensors") if args.backend == "lora" and not args.original_adapter else None,
              "metrics": {"routing_and_labels_passed": sum(all(r["checks"].values()) for r in rows),
                          "hypothetical_model_answers": sum(r["result"]["status"] == "hypothetical_generated" for r in rows),
                          "hypothetical_outlines": sum(r["result"]["status"] == "hypothetical_outline" for r in rows),
                          "three_part_model_answers": sum(r["three_parts_present"] for r in rows),
                          "labelled_precedents_found": sum(r["labelled_precedent_retrieved"] is True for r in rows),
                          "labelled_precedent_cases": sum(r["labelled_precedent_retrieved"] is not None for r in rows),
                          "hypothetical_raw_refusal_patterns": sum(r["raw_refusal_pattern"] for r in rows if r["case"]["expected_mode"] == "hypothetical" and not r["case"]["expected_abstain"]),
                          "speech_fabrication_patterns": sum(r["raw_speech_fabrication_pattern"] for r in rows)},
              "limitations": ["Routing checks do not establish persona fidelity or recommendation quality.",
                              "Refusal and fabrication regular expressions are incomplete diagnostics; inspect raw answers.",
                              "Hypothetical recommendations are interpretations, not historical facts or private thought transcripts.",
                              "The original factual adapter is preserved. A separate behavior adapter is trained on event/action/analogy targets.",
                              "Earthquake recommendations are not in behavior training questions or targets; the announced diagnostic is still not a blind external test."],
              "rows": rows}
    write_json(ROOT / args.output, report)
    print(report["metrics"], flush=True)


if __name__ == "__main__":
    main()
