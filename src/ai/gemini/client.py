from google import genai
from google.genai import types

from src.ai.config import PROJECT_ID, LOCATION, MODEL_ID
from src.ai.gemini.prompts import SYSTEM_PROMPT
from src.ai.tools.revenue import get_revenue_anomalies
from src.ai.tools.delivery import get_high_risk_shipments
from src.ai.tools.bigquery import query_bigquery
from src.ai.tools.knowledge import search_knowledge
from src.ai.tools.schema import get_bigquery_schema




client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)


def ask(question: str) -> str:
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=question,
        config=types.GenerateContentConfig(
            temperature=0.2,
            system_instruction=SYSTEM_PROMPT,
            tools=[
                get_bigquery_schema,
                query_bigquery,
                get_revenue_anomalies,
                get_high_risk_shipments,
                search_knowledge
            ]
        ),
    )

    return response.text