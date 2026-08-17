from google.adk.agents import LlmAgent

operations_agent = LlmAgent(
    name="operations_agent",
    model="gemini-2.5-flash",
    description="Investigates logistics and operational issues.",
    instruction="""
            You are the operations specialist.

            Focus on:
            - delivery-delay risk
            - carriers
            - shipments
            - warehouses
            - pipeline and operational issues

            Use evidence only.
            Clearly distinguish predictions from actual outcomes.
    """,
)