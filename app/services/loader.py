from langchain_community.document_loaders import PyPDFLoader
from app.core.logger import get_logger

logger = get_logger(__name__)

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    if not docs or all(not d.page_content.strip() for d in docs):
        logger.warning(f"No content found in PDF: {file_path}")
    return docs