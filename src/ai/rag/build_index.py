import json
from pathlib import Path

from src.ai.rag.loader import load_documents, chunk_documents
from src.ai.rag.embeddings import embed_document

INDEX_PATH = Path("enterprise_ai_retail_dataset/rag_index.json")


def build_index():
    chunks = chunk_documents(load_documents())
    index = []

    for i, chunk in enumerate(chunks, 1):
        print(f"Embedding {i}/{len(chunks)}")

        index.append({
            "source": chunk["source"],
            "text": chunk["text"],
            "embedding": embed_document(chunk["text"]),
        })

    INDEX_PATH.write_text(
        json.dumps(index),
        encoding="utf-8",
    )

    print(f"Saved {len(index)} chunks to {INDEX_PATH}")


if __name__ == "__main__":
    build_index()