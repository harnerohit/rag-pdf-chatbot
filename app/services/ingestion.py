from app.services.loader import load_pdf
from app.services.splitter import split_documents
from app.services.vectorstore import add_documents

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