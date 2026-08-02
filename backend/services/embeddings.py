from models import Chunk
from sentence_transformers import SentenceTransformer
from chromadb.api.types import Embedding

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: list[Chunk]) -> list[Embedding]:
    texts = [chunk.text for chunk in chunks]
   
    return model.encode(texts, show_progress_bar=True).tolist()

def embed_query(query: str) -> Embedding:
    
    return model.encode([query]).tolist()[0]