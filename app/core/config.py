from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    
    # API Keys
    groq_api_key: str
    
    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # LLM Configuration
    llm_model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.0
    max_tokens: int = 1024
    
    # ChromaDB
    chroma_persist_directory: str = "Chroma_db"
    
    # Text Splitting
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Retrieval
    retriever_top_k: int = 6
    
settings = Settings()