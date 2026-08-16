import json
import numpy as np
from pathlib import Path

from src.ai.rag.embeddings import embed_query

INDEX_PATH = Path("enterprise_ai_retail_dataset/rag_index.json")

chunks = json.loads(
    INDEX_PATH.read_text(encoding="utf-8")
)


def similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def retrieve(question: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed_query(question)

    scored = [
        (
            similarity(query_embedding, chunk["embedding"]),
            chunk,
        )
        for chunk in chunks
    ]

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "source": chunk["source"],
            "text": chunk["text"],
            "score": round(float(score), 4),
        }
        for score, chunk in scored[:top_k]
    ]