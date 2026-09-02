from models import Chunk
from sentence_transformers import SentenceTransformer
from chromadb.api.types import Embedding

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def embed_chunks(chunks: list[Chunk]) -> list[Embedding]:
    model = get_model()

    texts = [chunk.text for chunk in chunks]

    return model.encode(texts, show_progress_bar=True).tolist()


def embed_query(query: str) -> Embedding:
    model = get_model()

    return model.encode([query]).tolist()[0]