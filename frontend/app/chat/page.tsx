"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { askQuestion, ChatResponse } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  response?: ChatResponse;
}

function Chat() {
  const repo = useSearchParams().get("repo") ?? "";
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading || !repo) {
      return;
    }

    const userMessage: Message = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previous) => [...previous, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await askQuestion(repo, trimmedQuestion);

      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
        response,
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (err) {
      const errorMessage: Message = {
        role: "assistant",
        content:
          err instanceof Error
            ? `Error: ${err.message}`
            : "Something went wrong.",
      };

      setMessages((previous) => [...previous, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="chat-page">
      <header className="chat-header">
        <Link href="/" className="back-button">
          ← Repository
        </Link>

        <div className="chat-title">
          <div className="logo small">⌘</div>
          <span>{repo || "GitHub RAG Assistant"}</span>
        </div>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="empty-chat">
              <div className="empty-icon">⌕</div>

              <h2>{repo ? `Ask about ${repo}` : "No repository selected"}</h2>

              <p>
                {repo ? (
                  "Ask a question about the code, architecture, documentation, or implementation details."
                ) : (
                  <>
                    <Link href="/">Index a repository</Link> first, then ask
                    questions about it here.
                  </>
                )}
              </p>

              {repo && (
                <div className="example-questions">
                  <button
                    onClick={() => setQuestion("What does this project do?")}
                  >
                    What does this project do?
                  </button>

                  <button
                    onClick={() => setQuestion("How is the code structured?")}
                  >
                    How is the code structured?
                  </button>

                  <button
                    onClick={() => setQuestion("How do I run the tests?")}
                  >
                    How do I run the tests?
                  </button>
                </div>
              )}
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${
                message.role === "user" ? "user-message" : "assistant-message"
              }`}
            >
              <div className="message-label">
                {message.role === "user" ? "You" : "Assistant"}
              </div>

              <div className="message-content">{message.content}</div>

              {message.role === "assistant" &&
                message.response?.chunks &&
                message.response.chunks.length > 0 && (
                  <div className="sources">
                    <div className="sources-title">Sources</div>

                    {message.response.chunks.map((chunk) => (
                      <div
                        className="source"
                        key={`${chunk.source}-${chunk.chunk_index}`}
                      >
                        <span className="source-icon">📄</span>

                        <div>
                          <div className="source-name">{chunk.source}</div>

                          <div className="source-info">
                            Chunk {chunk.chunk_index}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
            </div>
          ))}

          {loading && (
            <div className="message assistant-message">
              <div className="message-label">Assistant</div>

              <div className="loading">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>

        <div className="input-container">
          <textarea
            placeholder="Ask something about the repository..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleAsk();
              }
            }}
            disabled={loading || !repo}
            rows={1}
          />

          <button
            className="send-button"
            onClick={handleAsk}
            disabled={loading || !repo || !question.trim()}
          >
            →
          </button>
        </div>

        <p className="input-hint">
          Press Enter to send · Shift + Enter for a new line
        </p>
      </div>
    </main>
  );
}

export default function ChatPage() {
  // useSearchParams needs a Suspense boundary for static builds
  return (
    <Suspense>
      <Chat />
    </Suspense>
  );
}
