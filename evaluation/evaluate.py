import asyncio
import json
import uuid
from pathlib import Path
import time
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.ai.agents.enterprise_operations_agent.agent import root_agent

from src.ai.observability.tracing import (
    RunTrace,
    ToolCall,
)

from src.ai.observability.metrics import (
    save_trace,
)

TEST_CASES = Path("evaluation/test_cases.json")
SAFETY_CASES = Path("evaluation/safety_cases.json")
RESULTS_FILE = Path("evaluation/results.json")

APP_NAME = "enterprise_ai_evaluation"
USER_ID = "evaluation_user"

MAX_RETRIES = 3


def contains_all(text: str, values: list[str]) -> bool:
    text = text.lower()
    return all(value.lower() in text for value in values)


def contains_any(text: str, values: list[str]) -> bool:
    text = text.lower()
    return any(value.lower() in text for value in values)


def contains_none(text: str, values: list[str]) -> bool:
    text = text.lower()
    return all(value.lower() not in text for value in values)


def is_quota_error(error: str) -> bool:
    return (
        "429" in error
        or "RESOURCE_EXHAUSTED" in error
        or "quota" in error.lower()
    )


async def execute_agent(
    question: str,
) -> dict:

    trace = RunTrace()

    session_service = (
        InMemorySessionService()
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    session = (
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=str(uuid.uuid4()),
        )
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=question
            )
        ],
    )

    response_parts = []

    active_tools = {}

    try:

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=message,
        ):

            trace.agent_steps += 1

            author = getattr(
                event,
                "author",
                None,
            )

            if author:
                trace.agents.add(
                    author
                )

            usage = getattr(
                event,
                "usage_metadata",
                None,
            )

            trace.add_usage(
                usage
            )

            if (
                not event.content
                or not event.content.parts
            ):
                continue

            for part in event.content.parts:

                if part.function_call:

                    tool_name = (
                        part.function_call.name
                    )

                    trace.tools.append(
                        tool_name
                    )

                    if (
                        tool_name
                        == "transfer_to_agent"
                    ):
                        trace.handoffs += 1

                    tool_call = ToolCall(
                        name=tool_name,
                        started_at=time.perf_counter(),
                    )

                    active_tools[
                        part.function_call.id
                    ] = tool_call

                    trace.tool_calls.append(
                        tool_call
                    )

                if part.function_response:

                    call_id = (
                        part.function_response.id
                    )

                    tool_call = (
                        active_tools.get(
                            call_id
                        )
                    )

                    if tool_call:

                        tool_call.duration_ms = (
                            round(
                                (
                                    time.perf_counter()
                                    - tool_call.started_at
                                )
                                * 1000,
                                2,
                            )
                        )

                        tool_call.status = (
                            "success"
                        )

                if (
                    part.text
                    and event.is_final_response()
                ):

                    response_parts.append(
                        part.text
                    )

        trace.finish(
            "success"
        )

    except Exception as e:

        trace.errors.append(
            str(e)
        )

        trace.finish(
            "error"
        )

        save_trace(
            trace.to_dict()
        )

        raise

    save_trace(
        trace.to_dict()
    )

    return {
        "response":
            "\n".join(
                response_parts
            ).strip(),

        "agents_used":
            sorted(
                trace.agents
            ),

        "tools_used":
            trace.tools,

        "observability":
            trace.to_dict(),
    }
async def run_agent(question: str) -> dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return await execute_agent(question)

        except Exception as e:
            error = str(e)

            if is_quota_error(error) and attempt < MAX_RETRIES:
                wait = 10 * (2 ** (attempt - 1))

                print(
                    f"Vertex AI quota issue. "
                    f"Retrying in {wait}s "
                    f"({attempt}/{MAX_RETRIES})..."
                )

                await asyncio.sleep(wait)
                continue

            raise


def check_expected_agents(
    actual_agents: list[str],
    case: dict,
) -> dict | None:
    expected = []

    if case.get("expected_agent"):
        expected.append(
            case["expected_agent"]
        )

    if case.get("expected_agents"):
        expected.extend(
            case["expected_agents"]
        )

    if not expected:
        return None

    actual_lower = {
        agent.lower()
        for agent in actual_agents
    }

    passed = all(
        agent.lower() in actual_lower
        for agent in expected
    )

    return {
        "check": "expected_agents",
        "passed": passed,
        "expected": expected,
        "actual": actual_agents,
    }


def check_expected_tools(
    actual_tools: list[str],
    case: dict,
) -> dict | None:
    expected = case.get(
        "expected_tools"
    )

    if not expected:
        return None

    actual_lower = {
        tool.lower()
        for tool in actual_tools
    }

    passed = all(
        tool.lower() in actual_lower
        for tool in expected
    )

    return {
        "check": "expected_tools",
        "passed": passed,
        "expected": expected,
        "actual": actual_tools,
    }


async def evaluate_case(case: dict) -> dict:
    print(f"\n=== {case['id']} ===")
    print(
        f"Question: {case['question']}"
    )

    try:
        result = await run_agent(
            case["question"]
        )

    except Exception as e:
        return {
            "id": case["id"],
            "status": "ERROR",
            "error": str(e),
        }

    response = result["response"]
    agents_used = result["agents_used"]
    tools_used = result["tools_used"]

    print("\nAgents:")
    print(agents_used)

    print("\nTools:")
    print(tools_used)

    print("\nResponse:")
    print(response)

    checks = []

    agent_check = check_expected_agents(
        agents_used,
        case,
    )

    if agent_check:
        checks.append(agent_check)

    tool_check = check_expected_tools(
        tools_used,
        case,
    )

    if tool_check:
        checks.append(tool_check)

    if case.get("must_include"):
        passed = contains_all(
            response,
            case["must_include"],
        )

        checks.append(
            {
                "check": "must_include",
                "passed": passed,
                "expected": case[
                    "must_include"
                ],
            }
        )

    if case.get("must_include_any"):
        passed = contains_any(
            response,
            case["must_include_any"],
        )

        checks.append(
            {
                "check": "must_include_any",
                "passed": passed,
                "expected": case[
                    "must_include_any"
                ],
            }
        )

    if case.get("must_not_include"):
        passed = contains_none(
            response,
            case["must_not_include"],
        )

        checks.append(
            {
                "check": "must_not_include",
                "passed": passed,
                "forbidden": case[
                    "must_not_include"
                ],
            }
        )

    if case.get(
        "must_include_sections"
    ):
        passed = contains_all(
            response,
            case[
                "must_include_sections"
            ],
        )

        checks.append(
            {
                "check": "required_sections",
                "passed": passed,
                "expected": case[
                    "must_include_sections"
                ],
            }
        )

    if not checks:
        status = "UNSCORED"

    elif all(
        check["passed"]
        for check in checks
    ):
        status = "PASS"

    else:
        status = "FAIL"

    return {
        "id": case["id"],
        "status": status,
        "checks": checks,
        "agents_used": agents_used,
        "tools_used": tools_used,
        "response": response,
    }


def load_cases() -> list[dict]:
    cases = []

    if TEST_CASES.exists():
        cases.extend(
            json.loads(
                TEST_CASES.read_text(
                    encoding="utf-8"
                )
            )
        )

    if SAFETY_CASES.exists():
        cases.extend(
            json.loads(
                SAFETY_CASES.read_text(
                    encoding="utf-8"
                )
            )
        )

    return cases


async def main():
    cases = load_cases()

    results = []

    for case in cases:
        result = await evaluate_case(
            case
        )

        results.append(result)

        print(
            f"\nResult: "
            f"{result['status']}"
        )

        # Small delay to reduce Vertex AI
        # rate-limit pressure.
        await asyncio.sleep(2)

    passed = sum(
        r["status"] == "PASS"
        for r in results
    )

    failed = sum(
        r["status"] == "FAIL"
        for r in results
    )

    errors = sum(
        r["status"] == "ERROR"
        for r in results
    )

    unscored = sum(
        r["status"] == "UNSCORED"
        for r in results
    )

    scored = passed + failed

    print("\n============================")
    print("       EVALUATION SUMMARY")
    print("============================")

    print(f"PASS:     {passed}")
    print(f"FAIL:     {failed}")
    print(f"ERROR:    {errors}")
    print(f"UNSCORED: {unscored}")

    if scored:
        score = (
            passed / scored
        ) * 100

        print(
            f"\nQuality score: "
            f"{score:.1f}%"
        )

    RESULTS_FILE.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"\nResults saved to "
        f"{RESULTS_FILE}"
    )


if __name__ == "__main__":
    asyncio.run(main())