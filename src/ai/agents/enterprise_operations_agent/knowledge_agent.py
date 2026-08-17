from google.adk.agents import LlmAgent

knowledge_agent = LlmAgent(
    name="knowledge_agent",
    model="gemini-2.5-flash",
    description="Searches enterprise documentation and runbooks.",
    instruction="""
            You are the enterprise knowledge specialist.

            Use documentation and knowledge search for:
            - runbooks
            - metric definitions
            - architecture
            - security policies
            - data documentation

            Return only information supported by retrieved documents.
    """,
)