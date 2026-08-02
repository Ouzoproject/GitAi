from models import Chunk
import chromadb
from chromadb.api.types import Metadata, Embedding

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="github_repository"
)

def store_chunks(
    chunks: list[Chunk],
    embeddings: list[Embedding]
) -> None:
    ids = [chunk.id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]
    metadatas: list[Metadata] = [
        {"source_file": chunk.source_file, 
         "chunk_index": chunk.chunk_index}
        for chunk in chunks
        
    ]
    
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


    