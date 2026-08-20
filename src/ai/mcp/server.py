from mcp.server.fastmcp import FastMCP

from src.ai.tools.bigquery import query_bigquery
from src.ai.tools.schema import get_bigquery_schema
from src.ai.tools.revenue import get_revenue_anomalies
from src.ai.tools.delivery import get_high_risk_shipments
from src.ai.tools.knowledge import search_knowledge
from src.ai.tools.pipeline import get_pipeline_health
from src.ai.tools.incidents import get_incidents
from src.ai.tools.delivery import (
    get_high_risk_shipments,
    get_delivery_outcomes,
)

mcp = FastMCP("enterprise-ai-operations")


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
@mcp.tool()
def pipeline_health(
    start_date: str,
    end_date: str,
    pipeline_name: str | None = None,
    limit: int = 50,
) -> dict:
    """Get pipeline failures, delays and freshness issues."""
    return get_pipeline_health(
        start_date,
        end_date,
        pipeline_name,
        limit,
    )


@mcp.tool()
def incidents(
    start_date: str,
    end_date: str,
    domain: str | None = None,
    limit: int = 20,
) -> dict:
    """Get known operational incidents."""
    return get_incidents(
        start_date,
        end_date,
        domain,
        limit,
    )


@mcp.tool()
def delivery_outcomes(
    country_code: str,
    start_date: str,
    end_date: str,
    limit: int = 50,
) -> dict:
    """Get actual shipment delivery outcomes."""
    return get_delivery_outcomes(
        country_code,
        start_date,
        end_date,
        limit,
    )