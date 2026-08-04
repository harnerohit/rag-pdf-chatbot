from pydantic import BaseModel

class AskRequest(BaseModel):
    doc_id: str
    question: str