# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.api.routes: before os import", flush=True)
import os
print("[startup] app.api.routes: after os import", flush=True)

print("[startup] app.api.routes: before shutil import", flush=True)
import shutil
print("[startup] app.api.routes: after shutil import", flush=True)

print("[startup] app.api.routes: before uuid import", flush=True)
import uuid
print("[startup] app.api.routes: after uuid import", flush=True)

print("[startup] app.api.routes: before FastAPI imports", flush=True)
from fastapi import APIRouter, HTTPException, UploadFile, File
print("[startup] app.api.routes: after FastAPI imports", flush=True)

print("[startup] app.api.routes: before Pydantic import", flush=True)
from pydantic import BaseModel
print("[startup] app.api.routes: after Pydantic import", flush=True)

print("[startup] app.api.routes: before ingestion import", flush=True)
from app.services.ingestion import ingest_pdf
print("[startup] app.api.routes: after ingestion import", flush=True)

print("[startup] app.api.routes: before rag_chain import", flush=True)
from app.services.rag_chain import get_answer
print("[startup] app.api.routes: after rag_chain import", flush=True)

print("[startup] app.api.routes: before vectorstore import", flush=True)
from app.services.vectorstore import delete_document
print("[startup] app.api.routes: after vectorstore import", flush=True)

print("[startup] app.api.routes: before APIRouter()", flush=True)
router = APIRouter()
print("[startup] app.api.routes: after APIRouter()", flush=True)


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
print("[startup] app.api.routes: before uploads directory creation", flush=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
print("[startup] app.api.routes: after uploads directory creation", flush=True)


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
