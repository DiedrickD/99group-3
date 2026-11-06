import argparse
import json
import re
import time
from pathlib import Path
from .data import ROOT, load_sources
from .prompt import messages_for
from .retrieval import Retriever

DISCLOSURE = "Historical simulation; generated text is not an authentic Lee Kuan Yew quotation."
ABSTAIN = "The current research notes do not provide enough evidence to answer this question. I would need an additional reliable source."


def policy(question):
    lowered = question.lower()
    if len(question) > 4000:
        return "input_limit"
    if re.search(r"ignore.{0,30}(instructions|rules)|reveal.{0,30}(prompt|secret)|pretend.{0,25}(real|actual)|without citations|fabricate.{0,20}quot", lowered):
        return "instruction_override"
    if re.search(r"verbatim|entire (chapter|book)|full (chapter|book)|quote.{0,15}(chapter|page)", lowered):
        return "quotation_request"
    if (re.search(r"\b20(?:1[6-9]|[2-9]\d)\b", lowered)
            and re.search(r"\b(speech|delivered|said|wrote|interview|endorsing)\b", lowered)
            and not re.search(r"\b(would|might|imagine|hypothetical)\b", lowered)):
        return "posthumous_attribution"
    return None


def is_extrapolation(question):
    return bool(re.search(r"\b(20(?:1[6-9]|[2-9]\d)|today|current|nowadays|chatgpt|generative ai|cryptocurrency|bitcoin)\b", question, re.I))


class Chatbot:
    def __init__(self, backend="notes", adapter=None, k=3, use_rag=True):
        if backend not in {"notes", "base", "lora"}:
            raise ValueError("Unknown backend")
        if k < 1:
            raise ValueError("k must be positive")
        self.backend, self.k, self.use_rag = backend, k, use_rag
        self.retriever, self.sources = Retriever(), load_sources()
        self.generator = None
        if backend != "notes":
            if backend == "lora":
                adapter = Path(adapter) if adapter else ROOT / "models/lky-lora"
                if not (adapter / "adapter_model.safetensors").exists():
                    raise FileNotFoundError("Train an adapter first: python -m lky.train")
            from .generator import LocalGenerator
            self.generator = LocalGenerator(adapter=adapter if backend == "lora" else None)

    def answer(self, question):
        started = time.perf_counter()
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must be a nonempty string")
        reason = policy(question)
        notes = [] if reason or not self.use_rag else self.retriever.search(question, self.k)
        # This lexical gate is intentionally simple; its score is not a confidence probability.
        sufficient = bool(notes and notes[0]["score"] >= 1.0)
        raw, fallback = "", False
        if reason or (self.use_rag and not sufficient):
            body = ABSTAIN
            status = "abstained"
        elif self.generator:
            raw = self.generator.generate(messages_for(question, notes))
            cited = set(re.findall(r"\[(N\d+)\]", raw))
            allowed = {n["note_id"] for n in notes}
            if self.use_rag and (not cited or not cited <= allowed):
                body = self.note_answer(notes)
                status, fallback = "notes_fallback", True
            else:
                body, status = raw, "generated"
        else:
            body, status = self.note_answer(notes), "source_notes"
        if is_extrapolation(question) and status != "abstained":
            body = "Modern application would be an extrapolation, not a documented view of Lee Kuan Yew.\n\n" + body
        cited = set(re.findall(r"\[(N\d+)\]", body))
        references = [{"note_id": n["note_id"], **self.sources[n["source_id"]]} for n in notes if n["note_id"] in cited]
        return {"question": question, "answer": body, "disclosure": DISCLOSURE,
                "backend": self.backend, "rag": self.use_rag, "status": status,
                "policy_reason": reason, "extrapolation": is_extrapolation(question),
                "retrieved": [n["note_id"] for n in notes], "references": references,
                "raw_generation": raw, "citation_fallback": fallback,
                "latency_seconds": round(time.perf_counter() - started, 3)}

    @staticmethod
    def note_answer(notes):
        if not notes:
            return ABSTAIN
        return "Source-note summary (paraphrases):\n\n" + "\n\n".join(f'{n["text"]} [{n["note_id"]}]' for n in notes[:2])


def render(result):
    text = result["disclosure"] + "\n\n" + result["answer"]
    if result["references"]:
        text += "\n\nSources:\n" + "\n".join(
            f'[{r["note_id"]}] {r["title"]} ({r["event_date"]}), {r["locator"]}\n{r["url"]}' for r in result["references"])
    return text


def main():
    parser = argparse.ArgumentParser(description=DISCLOSURE)
    parser.add_argument("--backend", choices=["notes", "base", "lora"], default="notes")
    parser.add_argument("--adapter")
    parser.add_argument("--question")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    bot = Chatbot(args.backend, args.adapter)
    if args.question:
        result = bot.answer(args.question)
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render(result))
        return
    print(DISCLOSURE + "\nEach turn is independent. Type /quit to exit.")
    while True:
        try:
            question = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break
        if question.strip() == "/quit":
            break
        if question.strip():
            print("\n" + render(bot.answer(question)))


if __name__ == "__main__":
    main()
