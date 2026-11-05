"""FastAPI endpoints for document ingestion and RAG questions."""

from functools import lru_cache
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from .config import settings
from .pipeline import RAGPipeline


app = FastAPI(
    title="Learning RAG API",
    description=(
        "A local learning API for document ingestion, semantic retrieval, "
        "source citations, and optional LLM answer generation."
    ),
    version="0.1.0",
)


@lru_cache(maxsize=1)
def get_pipeline() -> RAGPipeline:
    return RAGPipeline(settings)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    top_k: int = Field(default=4, ge=1, le=20)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "generation_configured": bool(
            settings.llm_base_url and settings.llm_model
        ),
    }


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    filename = Path(file.filename or "upload").name
    suffix = Path(filename).suffix.lower()
    if suffix not in {".pdf", ".txt", ".md"}:
        raise HTTPException(
            status_code=415,
            detail="Only PDF, TXT, and MD files are supported.",
        )

    content = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Upload is too large.")
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    upload_dir = settings.data_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_path = upload_dir / f"{uuid4().hex}{suffix}"
    stored_path.write_bytes(content)

    try:
        result = get_pipeline().ingest_file(stored_path)
        # Keep the original user filename as the source label in responses.
        # The file itself is stored under a random name to avoid path traversal
        # and collisions.
        result["source"] = filename
        return result
    except (ValueError, OSError) as error:
        stored_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/query")
def query_documents(request: QuestionRequest) -> dict:
    try:
        return get_pipeline().ask(request.question, top_k=request.top_k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
