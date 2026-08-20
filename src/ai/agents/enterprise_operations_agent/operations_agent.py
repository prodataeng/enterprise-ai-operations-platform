from google.adk.agents import LlmAgent

from .mcp_config import operations_tools


operations_agent = LlmAgent(
    name="operations_agent",
    model="gemini-2.5-flash",
    description="Investigates logistics and operational issues.",
    instruction="""
            You are the operations specialist.

            Use MCP tools for delivery risk, actual delivery outcomes,
            pipeline health, and incidents.

            Distinguish predictions from actual outcomes.
            Never modify operational data.
            Never invent incidents or delivery outcomes.
            Only report evidence returned by tools.
            """,
    tools=[operations_tools],
)