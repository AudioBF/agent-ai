from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Agent Ai"
    app_env: str = "development"
    groq_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()