import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.ai.agents.enterprise_operations_agent.agent import root_agent
from fastapi.middleware.cors import CORSMiddleware

APP_NAME = "enterprise_ai_operations"

app = FastAPI(
    title="Enterprise AI Operations API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    agents_used: list[str]
    tools_used: list[str]


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": APP_NAME,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=request.user_id,
        session_id=session_id,
    )

    if session is None:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id,
        )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=request.message
            )
        ],
    )

    response_parts = []
    agents_used = set()
    tools_used = []

    try:
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=message,
        ):
            if getattr(event, "author", None):
                agents_used.add(event.author)

            if not event.content or not event.content.parts:
                continue

            for part in event.content.parts:
                if part.function_call:
                    tools_used.append(
                        part.function_call.name
                    )

                if part.text and event.is_final_response():
                    response_parts.append(
                        part.text
                    )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        ) from e

    return ChatResponse(
        response="\n".join(response_parts).strip(),
        session_id=session_id,
        agents_used=sorted(agents_used),
        tools_used=tools_used,
    )