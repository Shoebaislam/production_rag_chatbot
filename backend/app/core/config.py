from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    collection_name: str = "documents"

    ollama_llm_model: str = "qwen2.5:0.5b"
    ollama_embed_model: str = "nomic-embed-text"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl_seconds: int = 3600

    class Config:
        env_file = "../.env"


settings = Settings()


llm_provider: str = "ollama"

ollama_base_url: str = "http://host.docker.internal:11434"

openai_api_key: str | None = None
openai_model: str = "gpt-4o-mini"