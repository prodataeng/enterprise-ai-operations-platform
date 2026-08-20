import json
from pathlib import Path


TRACE_FILE = Path(
    "evaluation/observability.jsonl"
)


def save_trace(trace: dict):
    TRACE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with TRACE_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(
                trace,
                ensure_ascii=False,
            )
            + "\n"
        )


def load_traces() -> list[dict]:
    if not TRACE_FILE.exists():
        return []

    traces = []

    with TRACE_FILE.open(
        encoding="utf-8"
    ) as file:

        for line in file:
            if line.strip():
                traces.append(
                    json.loads(line)
                )

    return traces


def calculate_metrics(
    traces: list[dict],
) -> dict:

    if not traces:
        return {}

    successful = [
        t for t in traces
        if t["status"] == "success"
    ]

    failed = [
        t for t in traces
        if t["status"] != "success"
    ]

    durations = [
        t["duration_ms"]
        for t in traces
        if t.get("duration_ms")
        is not None
    ]

    tokens = [
        t["tokens"]["total"]
        for t in traces
    ]

    tool_calls = [
        len(t["tool_calls"])
        for t in traces
    ]

    steps = [
        t["agent_steps"]
        for t in traces
    ]

    return {
        "requests":
            len(traces),

        "successful":
            len(successful),

        "failed":
            len(failed),

        "success_rate":
            round(
                len(successful)
                / len(traces),
                4,
            ),

        "avg_duration_ms":
            round(
                sum(durations)
                / len(durations),
                2,
            )
            if durations else 0,

        "avg_tokens":
            round(
                sum(tokens)
                / len(tokens),
                2,
            ),

        "avg_tool_calls":
            round(
                sum(tool_calls)
                / len(tool_calls),
                2,
            ),

        "avg_agent_steps":
            round(
                sum(steps)
                / len(steps),
                2,
            ),
    }