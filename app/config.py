import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    GITHUB_DEFAULT_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "codellama")

    class Config:
        env_file = ".env"

settings = Settings()