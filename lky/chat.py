import argparse
import json
import re
import time
from pathlib import Path
from .data import ROOT, load_sources
from .prompt import messages_for
from .retrieval import Retriever
from .persona import profile, posthumous_attribution, response_mode, select_principles

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
    return None


class Chatbot:
    def __init__(self, backend="notes", adapter=None, k=3, use_rag=True, enable_behavior=True):
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
            self.generator = LocalGenerator(adapter=adapter if backend == "lora" else None, enable_behavior=enable_behavior)

    def answer(self, question):
        started = time.perf_counter()
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must be a nonempty string")
        reason = policy(question)
        notes = [] if reason or not self.use_rag else self.retriever.search(question, self.k)
        direct_ids = [n["note_id"] for n in notes]
        mode = response_mode(question, bool(notes))
        if mode == "historical":
            years = re.findall(r"\b(?:19|20)\d{2}\b", question)
            if years:
                notes = [n for n in notes if any(year in n["text"] or year in self.sources[n["source_id"]]["event_date"] for year in years)]
        correction = ""
        correction_source = None
        principles = []
        if not reason and posthumous_attribution(question):
            correction = "Lee Kuan Yew died on 23 March 2015, so he could not have delivered the requested later speech. The response below considers the topic hypothetically."
            correction_source = profile()["biography"]
        if mode == "hypothetical" and not reason and self.use_rag:
            notes, principles = select_principles(question, notes, self.retriever.notes, self.k)
        # This lexical gate is intentionally simple; its score is not a confidence probability.
        sufficient = bool(notes and notes[0].get("score", 1.0) >= 1.0)
        raw, fallback = "", False
        if reason or (mode == "historical" and self.use_rag and not sufficient):
            body = ABSTAIN
            status = "abstained"
        elif self.generator:
            raw = self.generator.generate(messages_for(question, notes, mode, correction))
            cited = set(re.findall(r"\[([NC]\d+)\]", raw))
            allowed = {n["note_id"] for n in notes}
            if mode == "hypothetical":
                body = self.hypothetical_answer(raw, notes)
                status = "hypothetical_generated"
            elif self.use_rag and (not cited or not cited <= allowed):
                body = self.note_answer(notes)
                status, fallback = "notes_fallback", True
            else:
                body, status = raw, "generated"
        elif mode == "hypothetical":
            body, status = self.hypothetical_outline(principles), "hypothetical_outline"
        else:
            body, status = self.note_answer(notes), "source_notes"
        if mode == "hypothetical" and status != "abstained":
            body = "Hypothetical interpretation / extrapolation, not a documented view of Lee Kuan Yew.\n\n" + body
            if not notes:
                body += "\n\nNo matching historical evidence is supplied; this is a general style simulation."
            if principles:
                body += "\n\nHistorical basis (supports the principles, not this hypothetical conclusion):\n" + "\n".join(
                    f'- {p["summary"]} [{p["note_id"]}]' for p in principles)
            if correction:
                body = correction + "\n\n" + body
        cited = set(re.findall(r"\[([NC]\d+)\]", body))
        references = [{"note_id": n["note_id"], **self.sources[n["source_id"]]} for n in notes if n["note_id"] in cited]
        return {"runtime_policy": "v3", "question": question, "answer": body, "disclosure": DISCLOSURE,
                "generation_adapter": getattr(self.generator, "active_adapter", None),
                "backend": self.backend, "rag": self.use_rag, "status": status,
                "policy_reason": reason, "extrapolation": mode == "hypothetical",
                "response_mode": mode, "direct_retrieved": direct_ids,
                "principles": principles, "premise_correction": correction,
                "correction_source": correction_source,
                "retrieved": [n["note_id"] for n in notes], "references": references,
                "raw_generation": raw, "citation_fallback": fallback,
                "latency_seconds": round(time.perf_counter() - started, 3)}

    @staticmethod
    def note_answer(notes):
        if not notes:
            return ABSTAIN
        return "Source-note summary (paraphrases):\n\n" + "\n\n".join(f'{n["text"]} [{n["note_id"]}]' for n in notes[:2])

    @staticmethod
    def hypothetical_outline(principles):
        return ("Suggested approach (authored outline; no LLM used): I would define the practical objective, "
                "compare the available options, test a limited change and review its results. "
                "Consider the skills required, the costs of failure and the longer-term consequences.")

    @staticmethod
    def hypothetical_answer(raw, notes):
        # The model proposes the new action. Factual precedents are rendered
        # from the verified notes so a paraphrase cannot reverse their meaning.
        application = re.search(r"Application\s*:\s*(.*?)(?=\n\s*Limit\s*:|$)", raw, re.IGNORECASE | re.DOTALL)
        suggestion = application.group(1).strip() if application else raw.strip()
        suggestion = re.sub(r"\[(?:[NC]\d+|\d+)\]", "", suggestion).strip()
        cited = set(re.findall(r"\[([NC]\d+)\]", raw))
        precedents = [n for n in notes if n["note_id"] in cited] or notes[:1]
        if precedents:
            basis = "\n".join(f'{n["text"]} [{n["note_id"]}]' for n in precedents[:2])
        else:
            basis = "No historical precedent is supplied."
        return (f"Historical precedent (source notes): {basis}\n\n"
                f"Possible application (LLM-generated): {suggestion}\n\n"
                "Limit: An analogy identifies a possible approach, not proof of Lee's opinion. "
                "Differences in the new situation and relevant expertise still matter.")


def render(result):
    text = result["disclosure"] + "\n\n" + result["answer"]
    if result["references"]:
        text += "\n\nSources:\n" + "\n".join(
            f'[{r["note_id"]}] {r["title"]} ({r["event_date"]}), {r["locator"]}\n{r["url"]}' for r in result["references"])
    if result.get("correction_source"):
        source = result["correction_source"]
        text += f'\n\nBiographical source for the correction: {source["title"]}\n{source["url"]}'
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
