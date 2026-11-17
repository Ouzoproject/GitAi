from pydantic import BaseModel


class RepoRequest(BaseModel):
    url: str

class IndexResponse(BaseModel):
    status: str
    repo: str
    files_found: int
    found_files: list[str]
    chunks: int
    embeddings: int

class ChatRequest(BaseModel):
    repo: str  # "owner/repo" of an indexed repository
    question: str

class SourceChunk(BaseModel):
    source: str
    chunk_index: int
    text: str

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]
    chunks: list[SourceChunk]

class SourceFile(BaseModel):
    path: str
    content: str

class Chunk(BaseModel):
    id: str
    text: str
    source_file: str
    chunk_index: int

class RetrievedChunk(BaseModel):
    text: str
    source_file: str
    chunk_index: int
    distance: float
    rerank_score: float | None = None

class SearchResult(BaseModel):
    chunks: list[RetrievedChunk]

    @property
    def context(self) -> str:
        return "\n\n".join(chunk.text for chunk in self.chunks)

    @property
    def sources(self) -> list[str]:
        return sorted({chunk.source_file for chunk in self.chunks})