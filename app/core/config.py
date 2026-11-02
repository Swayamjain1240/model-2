from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Model 2 RAG System"
    environment: str = "local"
    debug: bool = False
    database_url: str = "sqlite:///./data/model2.db"
    secret_key: str = "replace-this-with-a-long-random-secret"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
