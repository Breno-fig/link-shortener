
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env_name: str = "Local" #default name of current enviroment
    base_url: str = "http://localhost:8000" #default app domain
    db_url: str = "sqlite:///./shortener.db" #default db address

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for:{settings.env_name}")
    return settings

