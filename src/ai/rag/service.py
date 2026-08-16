from src.ai.gemini.client import client
from src.ai.config import MODEL_ID
from src.ai.rag.retriever import retrieve


def ask_knowledge(question: str) -> str:
    docs = retrieve(question)

    context = "\n\n".join(
        f"SOURCE: {doc['source']}\n{doc['text']}"
        for doc in docs
    )

    prompt = f"""
Answer the question using only the provided context.

If the answer is not supported by the context, say that you do not
have enough evidence.

QUESTION:
{question}

CONTEXT:
{context}
"""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
    )

    return response.text