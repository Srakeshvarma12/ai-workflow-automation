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

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
