from src.ai.rag.retriever import retrieve


def search_knowledge(question: str, top_k: int = 5) -> dict:
    """Search enterprise documentation for relevant knowledge.

    Args:
        question: The information to search for in runbooks,
                  business definitions, architecture and policies.
        top_k: Maximum number of relevant document chunks to return.
    """

    results = retrieve(question, top_k)

    return {
        "results": [
            {
                "source": r["source"],
                "score": r["score"],
                "text": r["text"],
            }
            for r in results
        ]
    }