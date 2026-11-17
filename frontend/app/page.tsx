"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { indexRepository } from "@/lib/api";

export default function Home() {
  const router = useRouter();

  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [indexedRepo, setIndexedRepo] = useState("");

  async function handleIndex() {
    if (!repoUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setLoading(true);
    setMessage("");
    setError("");
    setIndexedRepo("");

    try {
      const result = await indexRepository(repoUrl);

      setIndexedRepo(result.repo);
      setMessage(`${result.repo} indexed successfully!`);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while indexing.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <div className="container home-container">
        <div className="hero">
          <div className="logo">⌘</div>

          <h1>GitHub RAG Assistant</h1>

          <p className="subtitle">
            Ask questions about any GitHub repository using AI.
          </p>
        </div>

        <div className="card">
          <label htmlFor="repo-url">GitHub Repository</label>

          <input
            id="repo-url"
            type="text"
            placeholder="https://github.com/owner/repository"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleIndex();
              }
            }}
            disabled={loading}
          />

          <button
            className="primary-button"
            onClick={handleIndex}
            disabled={loading}
          >
            {loading ? "Indexing repository..." : "Index Repository"}
          </button>

          {message && <div className="success-message">✓ {message}</div>}

          {error && <div className="error-message">{error}</div>}
        </div>

        {indexedRepo && (
          <>
            <div className="divider">
              <span>next</span>
            </div>

            <button
              className="secondary-button"
              onClick={() =>
                router.push(`/chat?repo=${encodeURIComponent(indexedRepo)}`)
              }
            >
              Chat with {indexedRepo} →
            </button>
          </>
        )}

        <div className="features">
          <div>
            <strong>1. Index</strong>
            <span>Clone and process a repository</span>
          </div>

          <div>
            <strong>2. Search</strong>
            <span>Retrieve relevant code and documentation</span>
          </div>

          <div>
            <strong>3. Ask</strong>
            <span>Get AI-powered answers</span>
          </div>
        </div>
      </div>
    </main>
  );
}
