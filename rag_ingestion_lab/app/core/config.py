from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv( "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/1",)

settings = Settings()