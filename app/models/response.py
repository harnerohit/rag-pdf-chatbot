from typing import List, Optional
from pydantic import BaseModel

class SourceChunk(BaseModel):
    doc_id: str
    filename: str
    page: Optional[int] = None
    chunk_index: int
    snippet: str
    score: Optional[float] = None


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    pages: int
    chunks_indexed: int


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]