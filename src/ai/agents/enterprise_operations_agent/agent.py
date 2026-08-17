import os
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

from .analytics_agent import analytics_agent
from .operations_agent import operations_agent
from .knowledge_agent import knowledge_agent


# repo/src/ai/agents/enterprise_operations_agent/agent.py
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


analytics_agent.tools = [analytics_tools]
operations_agent.tools = [operations_tools]
knowledge_agent.tools = [knowledge_tools]


root_agent = LlmAgent(
    name="enterprise_operations_agent",
    model="gemini-2.5-flash",
    description=(
        "Coordinator for enterprise retail and logistics investigations."
    ),
   instruction="""
You are the coordinator for enterprise retail and logistics root-cause investigations.

Delegate only to the specialists required for the question.

Specialists:
- analytics_agent: revenue, orders, trends, SQL analysis and revenue anomalies
- operations_agent: shipments, carriers, warehouses and delivery-risk signals
- knowledge_agent: runbooks, definitions, architecture and policies

For root-cause investigations, follow this process:

1. Establish the business symptom using analytics evidence.
2. Check whether the symptom is statistically anomalous when relevant.
3. Investigate operational signals that could contribute to the symptom.
4. Retrieve the relevant investigation runbook or business definitions.
5. Synthesize all evidence.

Your final response must separate:

CONFIRMED FACTS
- Only evidence directly returned by specialists/tools.

POSSIBLE CONTRIBUTORS
- Plausible explanations supported by some evidence but not proven causal.

GAPS
- Evidence still missing before a root cause can be confirmed.

RECOMMENDED NEXT ACTIONS
- Specific checks that follow logically from the evidence and runbook.

Never claim causation from correlation alone.
Never invent metrics, incidents or root causes.
Do not call every specialist unless their domain is relevant.
""",
    sub_agents=[
        analytics_agent,
        operations_agent,
        knowledge_agent,
    ],
)