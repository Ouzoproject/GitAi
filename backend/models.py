from pydantic import BaseModel


class RepoRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

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

class SearchResult(BaseModel):
    chunks: list[RetrievedChunk]

    @property
    def context(self) -> str:
        return "\n\n".join(chunk.text for chunk in self.chunks)

    @property
    def sources(self) -> list[str]:
        return sorted({chunk.source_file for chunk in self.chunks})