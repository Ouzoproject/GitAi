const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface IndexResponse {
  status: string;
  repo: string; // "owner/repo"
  files_found: number;
  found_files: string[];
  chunks: number;
  embeddings: number;
}

export interface ChatResponse {
  question: string;
  answer: string;
  sources: string[];
  chunks: {
    source: string;
    chunk_index: number;
    text: string;
  }[];
}

// FastAPI errors look like {"detail": "message"}; show just the message.
async function errorMessage(
  response: Response,
  fallback: string,
): Promise<string> {
  const text = await response.text();
  try {
    const body = JSON.parse(text);
    if (typeof body.detail === "string") return body.detail;
  } catch {
    // not JSON, use the raw text below
  }
  return text || fallback;
}

export async function indexRepository(repoUrl: string): Promise<IndexResponse> {
  const response = await fetch(`${API_URL}/index`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: repoUrl }),
  });

  if (!response.ok) {
    throw new Error(await errorMessage(response, "Failed to index repository"));
  }

  return response.json();
}

export async function askQuestion(
  repo: string,
  question: string,
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ repo, question }),
  });

  if (!response.ok) {
    throw new Error(await errorMessage(response, "Failed to get answer"));
  }

  return response.json();
}
