# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.services.embedding: before lru_cache import", flush=True)
from functools import lru_cache
print("[startup] app.services.embedding: after lru_cache import", flush=True)

print("[startup] app.services.embedding: before HuggingFaceEmbeddings import", flush=True)
from langchain_huggingface import HuggingFaceEmbeddings
print("[startup] app.services.embedding: after HuggingFaceEmbeddings import", flush=True)

print("[startup] app.services.embedding: before settings import", flush=True)
from app.core.config import settings
print("[startup] app.services.embedding: after settings import", flush=True)

@lru_cache
def get_embedding_function():
    """
    Returns a cached instance of the HuggingFaceEmbeddings class.
    This function uses LRU caching to avoid re-initializing the embeddings model multiple times.
    """
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
    )
