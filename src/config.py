from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env_name: str = "Local" #name of current enviroment
    base_url: str = "http://localhost:8000" #app domain
    db_url: str = "sqlite:///./shortener.db" #db address

def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for:{settings.env_name}")
    return settings
