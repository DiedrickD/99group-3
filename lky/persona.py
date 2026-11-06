"""Question routing and sourced principles for explicitly hypothetical answers."""
import json
import re
from .data import ROOT
from .retrieval import tokenize
from .router import predict


def profile():
    return json.loads((ROOT / "data/persona.json").read_text(encoding="utf-8"))


def posthumous_attribution(question):
    return bool(re.search(r"\b20(?:1[6-9]|[2-9]\d)\b", question, re.IGNORECASE)
                and re.search(r"\b(speech|delivered|said|wrote|interview|endorsing)\b", question, re.IGNORECASE)
                and not re.search(r"\b(would|might|imagine|hypothetical|if)\b", question, re.IGNORECASE))


def is_extrapolation(question):
    return bool(re.search(r"\b(20(?:1[6-9]|[2-9]\d)|today|current|nowadays|chatgpt|generative ai|cryptocurrency|bitcoin)\b", question, re.IGNORECASE))


def response_mode(question, has_evidence):
    if re.search(r"verbatim|entire (chapter|book)|full (chapter|book)", question, re.IGNORECASE):
        return "historical"
    if posthumous_attribution(question) or is_extrapolation(question):
        return "hypothetical"
    # Explicit advice and imagined applications can be useful without a matching speech.
    if re.search(r"\b(would|might|will|should|advice|advise|recommend|imagine|hypothetical)\b", question, re.IGNORECASE):
        return "hypothetical"
    if re.search(r"\b(what did|what was|when|where|who|how many|which speech|born|private conversation|favourite|favorite)\b", question, re.IGNORECASE):
        return "historical"
    return predict(question)


def select_principles(question, direct_notes, available_notes, k=3):
    persona = profile()
    note_map = {n["note_id"]: n for n in available_notes}
    query = set(tokenize(question))
    ranked = sorted(persona["principles"],
                    key=lambda p: (-len(query & set(p["keywords"])), p["id"]))
    matched = [p for p in ranked if query & set(p["keywords"])]
    if not matched:
        matched = [next(p for p in ranked if p["id"] == pid) for pid in persona["default_principles"]]
    notes, principles = [], []
    direct_ids = {n["note_id"] for n in direct_notes}
    # Topic metadata finds analogous principles rather than letting generic
    # word matches (for example 'services') crowd out the relevant precedent.
    matched.sort(key=lambda p: (-(len(query & set(p["keywords"])) + 0.5 * (p["note_id"] in direct_ids)), p["id"]))
    for principle in matched:
        nid = principle["note_id"]
        if nid in note_map and nid not in {n["note_id"] for n in notes} and len(notes) < k:
            notes.append(note_map[nid])
    for note in notes:
        principle = next((p for p in persona["principles"] if p["note_id"] == note["note_id"]), None)
        principles.append({"note_id": note["note_id"], "summary": principle["summary"] if principle else note["text"]})
    return notes, principles
