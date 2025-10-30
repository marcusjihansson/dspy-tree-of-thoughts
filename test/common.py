import json
import os
from pathlib import Path


def load_knowledge_base():
    texts = []
    data_dir = Path("data")
    for txt_file in data_dir.glob("*.txt"):
        texts.append(txt_file.read_text(encoding="utf-8"))
    return "\n\n".join(texts)


class SimpleRetriever:
    def __init__(self, text: str):
        self.chunks = text.split("\n\n")  # Split by paragraphs

    def retrieve(self, query: str, top_k: int = 3):
        query_words = set(query.lower().split())
        scores = []
        for chunk in self.chunks:
            chunk_words = set(chunk.lower().split())
            score = len(query_words.intersection(chunk_words))
            scores.append((score, chunk))
        scores.sort(reverse=True)
        return [chunk for _, chunk in scores[:top_k]]


PROFILE_PARAMS = {
    "easy": {"max_steps": 3, "n_select": 2},
    "smoke": {"max_steps": 4, "n_select": 2},
    "stress": {"max_steps": 6, "n_select": 3},
}


def load_queries(profile: str | None = None):
    with open("test/queries.json", "r", encoding="utf-8") as f:
        qs = json.load(f)
    if profile:
        return [q for q in qs if q["tier"] == profile]
    return qs


def get_profile():
    return os.getenv("PROFILE")  # easy / smoke / stress / None
