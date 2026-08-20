"use client";

import { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
  agents?: string[];
  tools?: string[];
};

export default function Home() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! Ask me about revenue, deliveries, incidents, or operational issues.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const [sessionId, setSessionId] = useState<string | null>(
    null
  );

  async function askAgent() {
    const text = question.trim();

    if (!text || loading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: text,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: text,
            user_id: "web-user",
            session_id: sessionId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();

      setSessionId(data.session_id);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.response,
          agents: data.agents_used,
          tools: data.tools_used,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "Something went wrong while investigating. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="mx-auto flex min-h-[90vh] max-w-3xl flex-col">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Enterprise AI Operations
          </h1>

          <p className="mt-2 text-gray-600">
            Ask about revenue, deliveries, incidents and operations.
          </p>
        </div>

        <div className="flex-1 space-y-5 rounded-xl bg-white p-6 shadow">
          {messages.map((message, index) => (
            <div
              key={index}
              className={
                message.role === "user"
                  ? "flex justify-end"
                  : "flex justify-start"
              }
            >
              <div
                className={
                  message.role === "user"
                    ? "max-w-[80%] rounded-2xl bg-black px-4 py-3 text-white"
                    : "max-w-[85%] rounded-2xl bg-gray-100 px-4 py-3 text-gray-900"
                }
              >
                <p className="whitespace-pre-wrap leading-7">
                  {message.content}
                </p>

                {message.role === "assistant" &&
                  ((message.agents?.length ?? 0) > 0 ||
                    (message.tools?.length ?? 0) > 0) && (
                    <details className="mt-4 border-t border-gray-300 pt-3 text-sm text-gray-500">
                      <summary className="cursor-pointer font-medium text-gray-700">
                        Investigation details
                      </summary>

                      {message.agents &&
                        message.agents.length > 0 && (
                          <div className="mt-3">
                            <span className="font-semibold text-gray-700">
                              Agents:
                            </span>{" "}
                            {message.agents.join(", ")}
                          </div>
                        )}

                      {message.tools &&
                        message.tools.length > 0 && (
                          <div className="mt-2">
                            <span className="font-semibold text-gray-700">
                              Tools:
                            </span>{" "}
                            {message.tools.join(", ")}
                          </div>
                        )}
                    </details>
                  )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="rounded-2xl bg-gray-100 px-4 py-3 text-gray-500">
                Investigating...
              </div>
            </div>
          )}
        </div>

        <div className="mt-4 flex gap-3">
          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="Ask something..."
            rows={2}
            className="flex-1 resize-none rounded-xl border border-gray-300 bg-white p-4 text-gray-900 outline-none focus:border-gray-500"
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey
              ) {
                event.preventDefault();
                askAgent();
              }
            }}
          />

          <button
            onClick={askAgent}
            disabled={loading}
            className="rounded-xl bg-black px-6 font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading ? "Working..." : "Send"}
          </button>
        </div>

        <p className="mt-3 text-center text-xs text-gray-500">
          AI responses are based on available enterprise data
          and evidence.
        </p>
      </div>
    </main>
  );
}