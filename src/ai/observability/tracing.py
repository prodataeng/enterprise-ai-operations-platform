import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    name: str
    started_at: float
    duration_ms: float | None = None
    status: str = "running"
    error: str | None = None


@dataclass
class RunTrace:
    request_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    started_at: float = field(
        default_factory=time.perf_counter
    )

    duration_ms: float | None = None
    status: str = "running"

    agents: set[str] = field(
        default_factory=set
    )

    tools: list[str] = field(
        default_factory=list
    )

    tool_calls: list[ToolCall] = field(
        default_factory=list
    )

    prompt_tokens: int = 0
    output_tokens: int = 0
    thought_tokens: int = 0
    total_tokens: int = 0

    llm_calls: int = 0
    agent_steps: int = 0
    handoffs: int = 0

    errors: list[str] = field(
        default_factory=list
    )

    def finish(
        self,
        status: str = "success",
    ):
        self.status = status

        self.duration_ms = round(
            (
                time.perf_counter()
                - self.started_at
            )
            * 1000,
            2,
        )

    def add_usage(
        self,
        usage: Any,
    ):
        if not usage:
            return

        self.llm_calls += 1

        self.prompt_tokens += (
            getattr(
                usage,
                "prompt_token_count",
                0,
            )
            or 0
        )

        self.output_tokens += (
            getattr(
                usage,
                "candidates_token_count",
                0,
            )
            or 0
        )

        self.thought_tokens += (
            getattr(
                usage,
                "thoughts_token_count",
                0,
            )
            or 0
        )

        self.total_tokens += (
            getattr(
                usage,
                "total_token_count",
                0,
            )
            or 0
        )

    def to_dict(self) -> dict:
        return {
            "request_id":
                self.request_id,

            "status":
                self.status,

            "duration_ms":
                self.duration_ms,

            "agents":
                sorted(self.agents),

            "tools":
                self.tools,

            "agent_steps":
                self.agent_steps,

            "handoffs":
                self.handoffs,

            "llm_calls":
                self.llm_calls,

            "tokens": {
                "prompt":
                    self.prompt_tokens,

                "output":
                    self.output_tokens,

                "thought":
                    self.thought_tokens,

                "total":
                    self.total_tokens,
            },

            "tool_calls": [
                {
                    "name": call.name,
                    "duration_ms":
                        call.duration_ms,
                    "status":
                        call.status,
                    "error":
                        call.error,
                }
                for call
                in self.tool_calls
            ],

            "errors":
                self.errors,
        }