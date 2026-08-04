import os
import shutil
import uuid

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.services.ingestion import ingest_pdf
from app.services.rag_chain import get_answer
from app.services.vectorstore import delete_document

router = APIRouter()


class AskRequest(BaseModel):
    doc_id: str
    question: str


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    pages: int
    chunks_indexed: int


class AskResponse(BaseModel):
    answer: str
    sources: list
    retrieved_chunks: int


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    doc_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{doc_id}.pdf",
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks, pages = ingest_pdf(
            file_path=file_path,
            doc_id=doc_id,
            filename=file.filename,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        pages=pages,
        chunks_indexed=chunks,
    )


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    answer, sources = get_answer(
        doc_id=request.doc_id,
        question=request.question,
    )

    return AskResponse(
        answer=answer,
        sources=sources,
        retrieved_chunks=len(sources),
    )


@router.delete("/delete/{doc_id}")
async def delete(doc_id: str):
    deleted = delete_document(doc_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return {"message": "Document deleted successfully."}