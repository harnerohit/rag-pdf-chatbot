# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.models.response: before typing import", flush=True)
from typing import List, Optional
print("[startup] app.models.response: after typing import", flush=True)

print("[startup] app.models.response: before Pydantic import", flush=True)
from pydantic import BaseModel
print("[startup] app.models.response: after Pydantic import", flush=True)

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
