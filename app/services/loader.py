# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.services.loader: before logger import", flush=True)
from app.core.logger import get_logger
print("[startup] app.services.loader: after logger import", flush=True)

print("[startup] app.services.loader: before logger creation", flush=True)
logger = get_logger(__name__)
print("[startup] app.services.loader: after logger creation", flush=True)

def load_pdf(file_path: str):
    print("[startup] app.services.loader: before PyPDFLoader import", flush=True)
    from langchain_community.document_loaders import PyPDFLoader
    print("[startup] app.services.loader: after PyPDFLoader import", flush=True)
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    if not docs or all(not d.page_content.strip() for d in docs):
        logger.warning(f"No content found in PDF: {file_path}")
    return docs
