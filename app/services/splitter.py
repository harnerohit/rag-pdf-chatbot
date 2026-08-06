# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.services.splitter: before settings import", flush=True)
from app.core.config import settings
print("[startup] app.services.splitter: after settings import", flush=True)

def split_documents(docs):
    print("[startup] app.services.splitter: before text splitter import", flush=True)
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("[startup] app.services.splitter: after text splitter import", flush=True)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(docs)
