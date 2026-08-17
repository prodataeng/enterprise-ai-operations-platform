from google.adk.agents import LlmAgent

analytics_agent = LlmAgent(
    name="analytics_agent",
    model="gemini-2.5-flash",
    description="Analyzes structured business data and revenue patterns.",
    instruction="""
            You are the analytics specialist.

            Use available MCP tools for:
            - BigQuery analytics
            - schema discovery
            - revenue anomaly detection

            Focus on revenue, orders, trends, comparisons and anomalies.

            Use evidence only.
            Never invent metrics or column names.
    """,
)