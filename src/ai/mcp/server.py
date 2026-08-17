from mcp.server import MCPServer

from src.ai.tools.bigquery import query_bigquery
from src.ai.tools.schema import get_bigquery_schema
from src.ai.tools.revenue import get_revenue_anomalies
from src.ai.tools.delivery import get_high_risk_shipments
from src.ai.tools.knowledge import search_knowledge


mcp = MCPServer("enterprise-ai-operations")


@mcp.tool()
def bigquery_query(sql: str) -> dict:
    """Run a safe read-only BigQuery analytical query."""
    return query_bigquery(sql)


@mcp.tool()
def bigquery_schema() -> dict:
    """Get approved BigQuery tables, columns and data types."""
    return get_bigquery_schema()


@mcp.tool()
def revenue_anomalies(
    country_code: str,
    limit: int = 10,
) -> dict:
    """Get ML-detected historical revenue anomalies."""
    return get_revenue_anomalies(
        country_code=country_code,
        limit=limit,
    )


@mcp.tool()
def delivery_risk(
    country_code: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 10,
) -> dict:
    """Get shipments with the highest predicted delay risk."""
    return get_high_risk_shipments(
        country_code=country_code,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )


@mcp.tool()
def knowledge_search(
    question: str,
    top_k: int = 5,
) -> dict:
    """Search enterprise runbooks, definitions and documentation."""
    return search_knowledge(
        question=question,
        top_k=top_k,
    )