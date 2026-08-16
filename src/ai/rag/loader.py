from pathlib import Path
import json

DOCS_PATH = Path("enterprise_ai_retail_dataset/docs")


def load_documents() -> list[dict]:
    docs = []

    for path in DOCS_PATH.rglob("*"):
        suffix = path.suffix.lower()

        if suffix in {".md", ".txt"}:
            text = path.read_text(encoding="utf-8")

        elif suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            text = json.dumps(data, indent=2)

        else:
            continue

        docs.append({
            "source": str(path),
            "text": text,
        })

    return docs


def chunk_documents(docs: list[dict], chunk_size: int = 1000) -> list[dict]:
    chunks = []

    for doc in docs:
        for i in range(0, len(doc["text"]), chunk_size):
            chunks.append({
                "source": doc["source"],
                "text": doc["text"][i:i + chunk_size],
            })

    return chunks