from chromadb.api.types import Embedding, QueryResult
from ingestion.vector_store import collection


def search(
    query_embedding: Embedding,
    k: int = 5,
)-> QueryResult:
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )