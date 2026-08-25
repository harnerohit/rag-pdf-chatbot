# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.core.config: before pydantic_settings import", flush=True)
from pydantic_settings import BaseSettings, SettingsConfigDict
print("[startup] app.core.config: after pydantic_settings import", flush=True)

print("[startup] app.core.config: before Settings class definition", flush=True)
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    
    # API Keys
    groq_api_key: str
    
    # Embedding Model
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    
    # LLM Configuration
    llm_model: str = "openai/gpt-oss-120b"
    temperature: float = 0.0
    max_tokens: int = 1024
    
    # ChromaDB
    chroma_persist_directory: str = "Chroma_db"
    
    # Text Splitting
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Retrieval
    retriever_top_k: int = 6

print("[startup] app.core.config: after Settings class definition", flush=True)
print("[startup] app.core.config: before Settings()", flush=True)
settings = Settings()
print("[startup] app.core.config: after Settings()", flush=True)
