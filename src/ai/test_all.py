from src.ai.tools.bigquery import query_bigquery
from src.ai.tools.schema import get_bigquery_schema
from src.ai.tools.revenue import get_revenue_anomalies
from src.ai.tools.delivery import get_high_risk_shipments
from src.ai.tools.knowledge import search_knowledge
from src.ai.gemini.client import ask


print("\n=== 1. BIGQUERY SCHEMA ===")
schema = get_bigquery_schema()
print(f"Tables found: {len(schema)}")
print(list(schema.keys())[:5])


print("\n=== 2. GENERIC BIGQUERY ===")
result = query_bigquery("""
SELECT
    country_code,
    SUM(net_revenue_sek) AS revenue
FROM `diesel-command-483009-r5.retail_ai_dev_ml.mart_daily_revenue`
WHERE date_key BETWEEN '2026-07-01' AND '2026-07-31'
GROUP BY country_code
ORDER BY revenue DESC
LIMIT 5
""")
print(result)


print("\n=== 3. REVENUE ANOMALIES ===")
print(
    get_revenue_anomalies(
        country_code="SE",
        limit=3
    )
)


print("\n=== 4. DELIVERY RISK ===")
print(
    get_high_risk_shipments(
        country_code="SE",
        start_date="2026-07-25",
        end_date="2026-07-31",
        limit=3
    )
)


print("\n=== 5. RAG KNOWLEDGE ===")
print(
    search_knowledge(
        "How should a revenue drop be investigated?",
        top_k=3
    )
)


print("\n=== 6. GEMINI ORCHESTRATION ===")
print(
    ask(
        """
Investigate Sweden's revenue performance between
2026-07-25 and 2026-07-31.

Use available data, anomaly detection, delivery-risk
predictions and the investigation documentation.

Tell me what deserves investigation based only on evidence.
"""
    )
)


print("\n=== ALL TESTS COMPLETED ===")