from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    opensearch_url: str = os.getenv("OPENSEARCH_URL", "http://localhost:9200")
    opensearch_index: str = os.getenv("OPENSEARCH_INDEX", "rag_chunks_1536_v1")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embedding_dimensions: int = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    chunk_tokens: int = int(os.getenv("MAX_CHUNK_TOKENS", "300"))
    overlap_tokens: int = int(os.getenv("CHUNK_OVERLAP_TOKENS", "40"))
    storage_dir: Path = Path(os.getenv("STORAGE_DIR", "storage"))

settings = Settings()