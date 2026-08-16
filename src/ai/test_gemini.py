from src.ai.gemini.client import ask


print(
    ask(
        """
Investigate Sweden's revenue performance at the end of July 2026.

Check:
- recent revenue
- whether revenue was anomalous
- delivery-delay risks during the same period
- our revenue investigation runbook

Based only on the available evidence, tell me what deserves investigation.
"""
    )
)