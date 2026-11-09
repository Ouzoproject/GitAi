from fastapi import FastAPI

from services.llm.query_rewriter import rewrite_query
from services.ingestion.vector_store import store_chunks
from services.retrieval.search import search
from services.ingestion.embeddings import embed_chunks, embed_query
from models import RepoRequest, ChatRequest, ChatResponse
from services.ingestion.loader import clone_repo, load_files
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

@app.post("/index")
async def index_repo(request: RepoRequest):
   
    path = clone_repo(request.url)

    files = load_files(path)

    chunks = chunk_files(files)

    embeddings = embed_chunks(chunks)

    store_chunks(chunks, embeddings)
    
    return {"status": "indexed", 
            "files found": len(files), 
            "found files": [file.path for file in files],
            "chunks": len(chunks),
            "embeddings": len(embeddings)}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print(f"Received search request for question: {request.question}")
    rewritten_query = rewrite_query(request.question)
    print("Embedding query")
    query_embedding = embed_query(rewritten_query)

    print("Searching for relevant chunks")

    results = search(query_embedding)    

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

