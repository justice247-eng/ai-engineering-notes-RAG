"""Document loading and simple, explainable text chunking."""

from hashlib import sha256
from pathlib import Path
import re

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def extract_text(path: str | Path) -> str:
    """Extract text from a PDF, plain-text, or Markdown file."""
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type {suffix!r}. Use PDF, TXT, or MD."
        )

    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = file_path.read_text(encoding="utf-8", errors="replace")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        raise ValueError(
            "No extractable text was found. Scanned PDFs need OCR first."
        )
    return text


def chunk_text(
    text: str, chunk_size: int = 180, overlap: int = 30
) -> list[str]:
    """Split text into word-based chunks with a configurable overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_size")

    words = text.split()
    chunks: list[str] = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap

    return chunks


def make_document_id(path: str | Path, source_name: str | None = None) -> str:
    """Create a stable identifier from file contents and its display name."""
    digest = sha256()
    digest.update(Path(path).read_bytes())
    digest.update((source_name or Path(path).name).encode("utf-8"))
    return digest.hexdigest()[:20]
