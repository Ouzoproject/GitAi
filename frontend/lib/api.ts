const API_URL = "http://localhost:8000";

export interface IndexResponse {
  message?: string;
  [key: string]: unknown;
}

export interface ChatResponse {
  question: string;
  answer: string;
  rewritten_query?: string | null;
  num_chunks?: number;
  chunks?: {
    rank: number;
    source: string;
    chunk_index: number;
    distance?: number;
    rerank_score?: number;
    text: string;
  }[];
}

export async function indexRepository(repoUrl: string): Promise<IndexResponse> {
  const response = await fetch(`${API_URL}/index`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: repoUrl,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to index repository");
  }

  return response.json();
}

export async function askQuestion(question: string): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to get answer");
  }

  return response.json();
}
