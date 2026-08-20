import os
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters


ROOT = Path(__file__).resolve().parents[4]

MCP_BIN = ROOT / ".venv" / "bin" / "mcp"
MCP_SERVER = ROOT / "src" / "ai" / "mcp" / "server.py"


mcp_connection = StdioConnectionParams(
    server_params=StdioServerParameters(
        command=str(MCP_BIN),
        args=[
            "run",
            str(MCP_SERVER),
        ],
        env={
            **os.environ,
            "PYTHONPATH": str(ROOT),
        },
    ),
    timeout=60,
)


analytics_tools = MCPToolset(
    connection_params=mcp_connection,
    tool_filter=[
        "bigquery_query",
        "bigquery_schema",
        "revenue_anomalies",
    ],
)


operations_tools = MCPToolset(
    connection_params=mcp_connection,
    tool_filter=[
        "bigquery_query",
        "bigquery_schema",
        "delivery_risk",
        "delivery_outcomes",
        "pipeline_health",
        "incidents",
    ],
)


knowledge_tools = MCPToolset(
    connection_params=mcp_connection,
    tool_filter=[
        "knowledge_search",
    ],
)