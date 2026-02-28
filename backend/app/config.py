from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Gemini
    GEMINI_API_KEY: str

    # Database
    DATABASE_URL: str

    # RabbitMQ
    RABBITMQ_URL: str

    # App
    SECRET_KEY: str = "changeme-in-production"
    ENVIRONMENT: str = "development"
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    # Prefect (optional)
    PREFECT_API_KEY: str = ""
    PREFECT_API_URL: str = ""

    # Render specific
    PYTHON_VERSION: Optional[str] = None

    model_config = {"env_file": ".env"}

settings = Settings()
