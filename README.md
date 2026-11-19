# GitHub RAG Assistant

A small RAG application that lets you ask questions about GitHub repositories. It retrieves relevant code and documentation and uses an LLM to generate answers based on the repository content.

## Features

- Index public GitHub repositories
- Extract and split source code and documentation into chunks
- Generate embeddings using Sentence Transformers
- Store and search embeddings with ChromaDB
- Improve retrieval with query rewriting and Cross-Encoder reranking
- Ask questions and receive AI-generated answers with source references

## Tech Stack

**Backend**

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Google Gemini API

**Frontend**

- Next.js
- React
- TypeScript

## How It Works

1. **Index Repository:** Enter a public GitHub repository URL. The application clones the repository and extracts supported files.
2. **Process Content:** Files are split into smaller chunks and converted into embeddings.
3. **Retrieve Relevant Content:** When you ask a question, the query is rewritten to improve search results. ChromaDB retrieves relevant chunks, which are then ranked using a Cross-Encoder.
4. **Generate Answer:** The retrieved content is sent to Gemini, which generates an answer based on the repository.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- Git
- A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/GitAi.git
cd GitAi
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory using `.env.example` as a template and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Start the backend:

```bash
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`.

### 3. Set Up the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

## Project Structure

```text
GitAi/
├── backend/
│   ├── services/
│   │   ├── ingestion/    # Repository loading, chunking and embeddings
│   │   ├── retrieval/    # Search, reranking and prompt building
│   │   └── llm/          # Gemini integration and query rewriting
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── lib/
│   └── package.json
│
└── README.md
```

## Notes

- The application currently supports `.py`, `.js`, `.ts`, `.tsx` and `.md` files.
- Indexed repositories and ChromaDB data are stored locally.
- The first run may take longer because the embedding and reranking models need to be downloaded.
- The application uses the Google Gemini API to generate answers. Questions and retrieved repository content are sent to Gemini, so avoid using sensitive code or private information.
