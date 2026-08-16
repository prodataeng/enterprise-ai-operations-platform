# AI and Data Access Policy

- Agents use least-privilege service accounts.
- Analytical tools are read-only unless a human explicitly approves a write action.
- Generated SQL is restricted to approved datasets.
- Destructive SQL is prohibited for autonomous agents.
- PII must not be surfaced without authorization.
- All tool calls must be logged.
