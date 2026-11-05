"""Environment-based configuration for the RAG application."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    chroma_path: Path
    collection_name: str
    embedding_model: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    max_upload_mb: int
    default_top_k: int

    @classmethod
    def from_env(cls) -> "Settings":
        data_dir = Path(os.getenv("RAG_DATA_DIR", "./data")).resolve()
        return cls(
            data_dir=data_dir,
            chroma_path=Path(
                os.getenv("CHROMA_PATH", str(data_dir / "chroma"))
            ).resolve(),
            collection_name=os.getenv("CHROMA_COLLECTION", "rag_documents"),
            embedding_model=os.getenv(
                "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
            ),
            llm_base_url=os.getenv("LLM_BASE_URL", "").rstrip("/"),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", ""),
            max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "15")),
            default_top_k=int(os.getenv("RAG_TOP_K", "4")),
        )


settings = Settings.from_env()
