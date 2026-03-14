"""Configuration management for the insurance chatbot."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Embedding Model (Free - sentence-transformers)
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")  # Free, local model
    # Note: embedding_dimension is auto-detected from model, but we set default for FAISS
    embedding_dimension: int = int(os.getenv("EMBEDDING_DIMENSION", "384"))  # Default for all-MiniLM-L6-v2
    
    # LLM Settings (Free - Ollama)
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "huggingface"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")  # or "mistral", "phi3", etc.
    
    # Hugging Face (alternative to Ollama)
    hf_model: str = os.getenv("HF_MODEL", "microsoft/Phi-3-mini-4k-instruct")
    hf_device: str = os.getenv("HF_DEVICE", "cpu")  # "cpu" or "cuda"
    
    # Vector Database
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./data/index/vector_db")
    
    # Retrieval Settings
    top_k_chunks: int = 5
    similarity_threshold: float = 0.7
    rerank_enabled: bool = True
    hybrid_search_enabled: bool = True
    hybrid_search_alpha: float = 0.7  # Weight for semantic search (0.7) vs keyword (0.3)
    
    # Chunking Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Data Paths
    raw_data_path: str = "./data/raw"
    processed_data_path: str = "./data/processed"
    
    # UHC Provider Settings
    uhc_base_url: str = "https://www.uhcprovider.com"
    uhc_policies_url: str = "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html"
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
