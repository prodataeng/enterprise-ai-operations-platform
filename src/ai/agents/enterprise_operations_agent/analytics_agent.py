from google.adk.agents import LlmAgent

from .mcp_config import analytics_tools


analytics_agent = LlmAgent(
    name="analytics_agent",
    model="gemini-2.5-flash",
    description="Analyzes structured business data and revenue patterns.",
    instruction="""
            You are the analytics specialist.

            Use MCP tools for BigQuery analytics, schema discovery,
            and revenue anomaly detection.

            Use bigquery_schema when you do not know the schema.
            Never invent table or column names.
            Never expose personally identifiable customer information.
            Use aggregated business metrics whenever possible.
            BigQuery access is strictly read-only.
            """,
    tools=[analytics_tools],
)