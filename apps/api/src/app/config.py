from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_name: str = "DocuMind"
    app_env: Literal["development", "production"] = "development"
    app_port: int = 8000
    app_log_level: str = "info"
    app_secret_key: str = "change-me-to-random-string"
    app_cors_origins: str = "http://localhost:3000"

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "documind"
    postgres_user: str = "documind"
    postgres_password: str = "changeme"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Vector Store
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "documind_chunks"

    # LLM Provider
    llm_provider: Literal["openai", "anthropic", "ollama"] = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_temperature: float = 0.1
    llm_max_tokens: int = 2000

    # Embedding Provider
    embedding_provider: Literal["openai", "ollama", "local"] = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_api_key: str = ""
    embedding_base_url: str = ""
    embedding_dimensions: int = 1536

    # RAG Settings
    rag_chunk_size: int = 1000
    rag_chunk_overlap: int = 200
    rag_top_k: int = 5
    rag_score_threshold: float = 0.7

    # Storage
    upload_dir: str = "/data/uploads"
    max_file_size_mb: int = 50
    allowed_file_types: str = "pdf,docx,txt,md"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_llm_model: str = "llama3.1"
    ollama_embed_model: str = "nomic-embed-text"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.app_cors_origins.split(",")]

    @property
    def allowed_extensions(self) -> list[str]:
        return [ext.strip() for ext in self.allowed_file_types.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
