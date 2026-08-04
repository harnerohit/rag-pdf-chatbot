from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

@lru_cache
def get_embedding_function():
    """
    Returns a cached instance of the HuggingFaceEmbeddings class.
    This function uses LRU caching to avoid re-initializing the embeddings model multiple times.
    """
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
    )