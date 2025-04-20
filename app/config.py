# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API settings
    API_TITLE: str = "Secure RAG System"
    API_VERSION: str = "0.1.0"
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4"
    
    # Vector DB settings
    VECTOR_DB_TYPE: str = "pinecone"  # Options: "pinecone", "weaviate"
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "secure-rag")
    
    # Security settings
    ENABLE_PRE_RETRIEVAL: bool = True
    ENABLE_VECTOR_SECURITY: bool = True
    ENABLE_POST_RETRIEVAL: bool = True
    ENABLE_MONITORING: bool = True
    
    # Similarity threshold
    MIN_SIMILARITY_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"
        
settings = Settings()