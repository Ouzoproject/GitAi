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