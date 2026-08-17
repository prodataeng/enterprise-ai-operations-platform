import os
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters


ROOT = Path(__file__).resolve().parents[4]

MCP_BIN = ROOT / ".venv" / "bin" / "mcp"
MCP_SERVER = ROOT / "src" / "ai" / "mcp" / "server.py"


mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
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
)


root_agent = LlmAgent(
    name="enterprise_operations_agent",
    model="gemini-2.5-flash",
    description="Enterprise retail and logistics operations assistant.",
    instruction="""
You are an enterprise retail and logistics AI operations agent.

Use the available MCP tools to investigate business and operational issues.

Use:
- bigquery_query for structured analytics
- bigquery_schema when schema is uncertain
- revenue_anomalies for ML-based revenue anomalies
- delivery_risk for predicted shipment delay risk
- knowledge_search for runbooks and enterprise documentation

Gather evidence before answering.
Never invent metrics, incidents, or root causes.
Clearly distinguish facts from hypotheses.
""",
    tools=[mcp_tools],
)