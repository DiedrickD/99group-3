"""Small, auditable BM25 index. No hidden downloads or API credentials."""
import math
import re
from collections import Counter
from .data import load_notes

STOP = set("a an the and or of to in for on with is are was were be been as at by from this that it its i me my you your he his we our would could should do does did what how why when who which about tell explain say said lee kuan yew singapore please can more than have has had into also".split())
STOP.update("s t re ve ll d us speech speeches address addresses account view views give exact delivered".split())


def tokenize(text):
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP]


class Retriever:
    def __init__(self, notes=None):
        self.notes = load_notes() if notes is None else notes
        self.tokens = [tokenize(row["text"] + " " + " ".join(row["tags"])) for row in self.notes]
        self.tf = [Counter(tokens) for tokens in self.tokens]
        self.df = Counter(token for tokens in self.tokens for token in set(tokens))
        self.avg = sum(map(len, self.tokens)) / max(1, len(self.tokens))

    def search(self, question, k=3):
        if k < 1:
            raise ValueError("k must be positive")
        query = set(tokenize(question))
        results = []
        for note, counts, tokens in zip(self.notes, self.tf, self.tokens):
            score = 0.0
            matches = query & counts.keys()
            for term in matches:
                frequency = counts[term]
                idf = math.log(1 + (len(self.notes) - self.df[term] + 0.5) / (self.df[term] + 0.5))
                score += idf * frequency * 2.5 / (frequency + 1.5 * (0.25 + 0.75 * len(tokens) / max(self.avg, 1)))
            if score > 0:
                results.append({**note, "score": round(score, 6), "matched_terms": sorted(matches)})
        results = sorted(results, key=lambda row: (-row["score"], row["note_id"]))
        if not results:
            return []
        cutoff = max(1.0, results[0]["score"] * 0.4)
        return [row for row in results if row["score"] >= cutoff][:k]
