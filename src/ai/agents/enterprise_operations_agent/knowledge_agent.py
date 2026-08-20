from google.adk.agents import LlmAgent

from .mcp_config import knowledge_tools


knowledge_agent = LlmAgent(
    name="knowledge_agent",
    model="gemini-2.5-flash",
    description="Searches enterprise documentation and runbooks.",
    instruction="""
You are the enterprise knowledge specialist.

Use knowledge_search for runbooks, definitions,
architecture, security policies, and documentation.
""",
    tools=[knowledge_tools],
)