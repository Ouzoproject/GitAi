from fastapi import FastAPI

from services.ingestion.vector_store import store_chunks
from services.retrieval.search import search
from services.ingestion.embeddings import embed_chunks, embed_query
from models import RepoRequest, ChatRequest, ChatResponse
from services.loader import clone_repo, load_files
from services.ingestion.chunking import chunk_files

app = FastAPI()

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

    query_embedding = embed_query(request.question)

    results = search(query_embedding, k=5)

  