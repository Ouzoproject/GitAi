# GitHub RAG Assistant

A small RAG (retrieval-augmented generation) app for asking questions about a public GitHub repository. It clones the repo, indexes its code and docs, retrieves the most relevant chunks for your question, and has Google Gemini answer from them.

## Features

- Index public GitHub repositories
- Split source code and documentation into chunks
- Generate embeddings with Sentence Transformers (`all-MiniLM-L6-v2`)
- Store and search embeddings with ChromaDB
- Improve retrieval with LLM query rewriting and Cross-Encoder reranking (`ms-marco-MiniLM-L6-v2`)
- Get answers with the retrieved source chunks shown alongside

## Tech Stack

**Backend:** Python, FastAPI, ChromaDB, Sentence Transformers, LangChain text splitters, Google Gemini API
**Frontend:** Next.js, React, TypeScript, Tailwind CSS

## How It Works

1. **Index:** Enter a public GitHub repository URL. The backend shallow-clones it and reads the supported files.
2. **Process:** Files are split into chunks and converted into embeddings, stored in a local ChromaDB collection (one per repository).
3. **Retrieve:** Your question is rewritten into search keywords by Gemini, the 40 closest chunks are fetched from ChromaDB, and a Cross-Encoder reranks them down to the top 5.
4. **Answer:** The top chunks and your question are sent to Gemini, which answers based only on that content.

## Getting Started

### Prerequisites

- Python 3.11 or newer
- Node.js 20.9 or newer (with npm)
- Git
- A [Google Gemini API key](https://aistudio.google.com/apikey)
- A few GB of free disk space (PyTorch and the two models are downloaded on first use)

### 1. Clone this repository

```bash
git clone https://github.com/Ouzoproject/GitAi.git
cd GitAi
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Linux / macOS:** `source .venv/bin/activate`

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create your `.env` file from the template and add your key:

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

```env
GEMINI_API_KEY=your_api_key_here
```

Start the backend **from the `backend` directory** (the `repos/` and `chroma_db/` folders are created relative to where you start it):

```bash
uvicorn main:app --reload
```

The API runs at `http://localhost:8000` (interactive docs at `/docs`). Don't add `--host 0.0.0.0`.

### 3. Set up the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` (use `localhost`, not `127.0.0.1`, because the backend only allows that origin).

If the backend runs somewhere other than `http://localhost:8000`, set `NEXT_PUBLIC_API_URL` in `frontend/.env.local`.

## Project Structure

```text
GitAi/
├── backend/
│   ├── services/
│   │   ├── ingestion/    # Cloning, chunking, embeddings, vector store
│   │   ├── retrieval/    # Search, reranking, prompt building
│   │   └── llm/          # Gemini client and query rewriting
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   ├── lib/
│   └── package.json
└── README.md
```

## Notes

- Supported file types: `.py`, `.js`, `.ts`, `.tsx`, `.md`. The folders `.git`, `node_modules`, `dist`, `build`, `venv`, `.venv`, `__pycache__` and `docs_src` are skipped.
- Cloned repositories are stored in `backend/repos/` and the vector database in `backend/chroma_db/`. Re-indexing a repository replaces its previous index. Delete these folders to reset everything.
- The first run is slow because the embedding and reranking models are downloaded.
- Questions, rewritten queries and retrieved repository content are sent to the Gemini API. Don't index code you aren't allowed to share with Google, and check Google's terms for how your API tier handles submitted data.

## Security notes

- The backend has no authentication. Anyone who can reach port 8000 can trigger clones and spend your Gemini quota, so keep it bound to localhost.
- Never commit your `.env` file. It is listed in `.gitignore`; only `.env.example` belongs in the repository.
- Only index repositories you trust. Repository content is passed into an LLM prompt and can contain instructions aimed at the model.

## License

No license yet
