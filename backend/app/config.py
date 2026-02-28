from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Gemini
    GEMINI_API_KEY: str

    # Database
    DATABASE_URL: str

    # RabbitMQ
    RABBITMQ_URL: str

    # App
    SECRET_KEY: str = "changeme-in-production"
    ENVIRONMENT: str = "production"
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    # Prefect (optional)
    PREFECT_API_KEY: str = ""
    PREFECT_API_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
