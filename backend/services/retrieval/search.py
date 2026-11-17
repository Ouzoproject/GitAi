from chromadb.api.models.Collection import Collection
from chromadb.api.types import Embedding
from models import RetrievedChunk, SearchResult
from typing import cast

def search(
    collection: Collection,
    query_embedding: Embedding,
    k: int = 40,
) -> SearchResult:
    count = collection.count()
    if count == 0:
        return SearchResult(chunks=[])

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, count),
    )

    if not results["documents"] or not results["metadatas"] or not results["distances"]:
        return SearchResult(chunks=[])

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = [
        RetrievedChunk(
            text=doc,
            source_file=cast(str, meta["source_file"]),
            chunk_index=cast(int, meta["chunk_index"]),
            distance=cast(float, distance)
        )
        for doc, meta, distance in zip(documents, metadatas, distances)
    ]

    return SearchResult(chunks=chunks)