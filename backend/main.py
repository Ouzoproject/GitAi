from fastapi import FastAPI, HTTPException
from git.exc import GitCommandError

from services.llm.query_rewriter import rewrite_query
from services.ingestion.vector_store import get_collection, store_chunks
from services.retrieval.search import search
from services.ingestion.embeddings import embed_chunks, embed_query
from models import RepoRequest, IndexResponse, ChatRequest, ChatResponse
from services.ingestion.loader import (
    InvalidRepoURL,
    clone_repo,
    load_files,
    parse_github_url,
    parse_repo_id,
)
from services.ingestion.chunking import chunk_files
from services.retrieval.reranker import rerank
from services.llm.client import llm_answer
from services.retrieval.prompt_builder import build_prompt

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def read_health():
    return {"status": "ok"}

@app.post("/index", response_model=IndexResponse)
async def index_repo(request: RepoRequest):

    try:
        owner, repo = parse_github_url(request.url)
        path = clone_repo(request.url)
    except InvalidRepoURL as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GitCommandError:
        raise HTTPException(
            status_code=400,
            detail="Could not clone the repository. Make sure it exists and is public.",
        )

    files = load_files(path)

    chunks = chunk_files(files)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No supported files found in this repository "
                   "(supported: .py, .js, .ts, .tsx, .md).",
        )

    embeddings = embed_chunks(chunks)

    repo_id = f"{owner}/{repo}"
    store_chunks(repo_id, chunks, embeddings)

    return {"status": "indexed",
            "repo": repo_id,
            "files_found": len(files),
            "found_files": [file.path for file in files],
            "chunks": len(chunks),
            "embeddings": len(embeddings)}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        parse_repo_id(request.repo)
    except InvalidRepoURL:
        raise HTTPException(
            status_code=400,
            detail="Invalid repository. Use the format owner/repository.",
        )

    collection = get_collection(request.repo)
    if collection is None:
        raise HTTPException(
            status_code=404,
            detail=f"{request.repo} has not been indexed yet. Index it first.",
        )

    print(f"Received search request for question: {request.question}")
    rewritten_query = rewrite_query(request.question)
    print("Embedding query")
    query_embedding = embed_query(rewritten_query)

    print("Searching for relevant chunks")

    results = search(collection, query_embedding)    

    print(f"Found {len(results.chunks)} chunks for query: {request.question}")
        
    print("reranking results")
    final_results = rerank(rewritten_query, results)
    print(final_results)
    print("Building prompt for LLM")
    prompt = build_prompt(request.question, final_results.context)
    print("calling llm")
    answer = llm_answer(prompt)
    print(f"Answer: {answer}")

    return {
        "question": request.question,
        "answer": answer,
        "sources": final_results.sources,
        "chunks": [
            {
                "source": chunk.source_file,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
            }
            for chunk in final_results.chunks
        ],
    }