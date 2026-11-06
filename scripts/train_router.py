import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lky.router import train_router


def main():
    factual = [
        "When was Lee born?", "What did Lee say about English?", "What happened at Bukit Ho Swee in 1961?",
        "Which speech discussed national reserves?", "What did the 2011 GIC address say?", "Who succeeded Lee as prime minister?",
        "What was the date of the fire?", "How did Lee describe British withdrawal?", "What did Lee say about bilingual education?",
        "What did Lee do after the fire?", "Where was the 1984 dinner held?", "Why was English useful as a working language?",
        "What is the historical evidence about his policy?", "Give the source for that quotation.", "What did the NTUC speech discuss?",
        "What was his stated view on corruption?", "How did he describe succession?", "What happened after separation?",
        "What were the proposals in the 1975 debate?", "How many people were displaced?", "Did Lee give this interview?",
        "Was that actually said by Lee?", "What is recorded about the event?", "Which document supports that historical claim?",
    ]
    hypothetical = [
        "What would Lee do about a new crisis?", "How might Lee respond to an unfamiliar situation?", "What should a leader do now?",
        "What will Lee do about a big eartquake?", "What would Lee advise my company?", "Imagine Lee addressing a future disaster.",
        "How would he handle a new technology?", "Should I change my career?", "What might he think about ChatGPT?",
        "How would Lee approach an ethical dilemma?", "What would Lee do if a manager failed?", "What might he advise a divided team?",
        "How could his approach apply to AI?", "Give a Lee-inspired response to an economic crisis.", "What might he recommend about remote work?",
        "What would his approach look like today?", "How might a small country handle a new conflict?", "What should we learn from his actions?",
        "How can that historical response apply to a new event?", "What would you do in my position?", "What is a hypothetical policy response?",
        "How might he assess a startup?", "What would he consider before changing policy?", "Apply his leadership style to this scenario.",
    ]
    rows = [{"question": question, "label": label} for label, questions in [("historical", factual), ("hypothetical", hypothetical)] for question in questions]
    (ROOT / "data/router_train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8", newline="\r\n")
    train_router()
    print(f"Trained intent router on {len(rows)} authored labelled examples; deterministic rules handle explicit and false-premise requests first.")


if __name__ == "__main__":
    main()
