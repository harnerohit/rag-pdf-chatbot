# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.services.ingestion: before loader import", flush=True)
from app.services.loader import load_pdf
print("[startup] app.services.ingestion: after loader import", flush=True)

print("[startup] app.services.ingestion: before splitter import", flush=True)
from app.services.splitter import split_documents
print("[startup] app.services.ingestion: after splitter import", flush=True)

print("[startup] app.services.ingestion: before vectorstore import", flush=True)
from app.services.vectorstore import add_documents
print("[startup] app.services.ingestion: after vectorstore import", flush=True)

def ingest_pdf(file_path: str, doc_id: str, filename: str):
    docs = load_pdf(file_path)
    
    if not docs or all(not doc.page_content.strip() for doc in docs):
        raise ValueError("The PDF file is empty or contains no readable text.")
    
    chunks = split_documents(docs)
    
    chunk_count = add_documents(
        doc_id=doc_id,
        filename=filename,
        chunks=chunks
    )
    
    return chunk_count,len(docs)
