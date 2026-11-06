"""A tiny learned intent classifier; its scores are not factual truth probabilities."""
import json
import math
import re
from collections import Counter
from .data import ROOT, digest, read_jsonl, write_json


def features(question):
    words = re.findall(r"[a-z]+", question.lower())
    return words + [a + " " + b for a, b in zip(words, words[1:])]


def train_router():
    examples = read_jsonl(ROOT / "data/router_train.jsonl")
    counts = {label: Counter() for label in ["historical", "hypothetical"]}
    documents = Counter()
    for row in examples:
        documents[row["label"]] += 1
        counts[row["label"]].update(features(row["question"]))
    write_json(ROOT / "models/router.json", {"type": "multinomial_naive_bayes", "training_examples": len(examples),
               "training_data_sha256": digest(ROOT / "data/router_train.jsonl"),
               "documents": dict(documents), "counts": {label: dict(values) for label, values in counts.items()}})


def predict(question):
    path = ROOT / "models/router.json"
    if not path.exists():
        return "hypothetical"
    artifact = json.loads(path.read_text(encoding="utf-8"))
    vocabulary = {token for counts in artifact["counts"].values() for token in counts}
    scores = {}
    for label, counts in artifact["counts"].items():
        score = math.log(artifact["documents"][label] / sum(artifact["documents"].values()))
        denominator = sum(counts.values()) + len(vocabulary)
        for token in features(question):
            if token in vocabulary:
                score += math.log((counts.get(token, 0) + 1) / denominator)
        scores[label] = score
    return max(scores, key=scores.get)
