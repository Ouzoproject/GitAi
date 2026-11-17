const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface IndexResponse {
  status: string;
  "files found": number;
  "found files": string[];
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

export async function indexRepository(repoUrl: string): Promise<IndexResponse> {
  const response = await fetch(`${API_URL}/index`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: repoUrl }),
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
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to get answer");
  }

  return response.json();
}
