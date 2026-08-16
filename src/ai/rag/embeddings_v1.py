from google import genai
from google.genai import types

from src.ai.config import PROJECT_ID, LOCATION, EMBEDDING_MODEL

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)

def embed_document(text: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768,
        ),
    )
    return response.embeddings[0].values


def embed_query(text: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768,
        ),
    )
    return response.embeddings[0].values