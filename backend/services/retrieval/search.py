from chromadb.api.types import Embedding
from models import RetrievedChunk, SearchResult
from services.ingestion.vector_store import collection
from typing import cast

def search(query_embedding: Embedding, k: int = 5) -> SearchResult:
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    if not results["documents"] or not results["metadatas"] or not results["distances"]:
        return SearchResult(chunks=[])
    

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]    
    distances = results["distances"][0]

    
    chunks=[
        RetrievedChunk(
            text=doc,
            source_file=cast(str, meta["source_file"]),
            chunk_index=cast(int, meta["chunk_index"]),
            distance=cast(float, distance)
        )
        for doc, meta, distance in zip(documents, metadatas, distances)
    ]
    

    return SearchResult(chunks=chunks)