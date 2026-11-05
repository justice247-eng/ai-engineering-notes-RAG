"""Orchestrates ingestion, retrieval, citations, and optional generation."""

from pathlib import Path

from .config import Settings
from .generator import OpenAICompatibleGenerator
from .ingestion import chunk_text, extract_text, make_document_id
from .store import VectorStore


class RAGPipeline:
    def __init__(self, config: Settings):
        self.config = config
        self.store = VectorStore(config)
        self.generator = OpenAICompatibleGenerator(config)

    def ingest_file(self, path: str | Path) -> dict:
        file_path = Path(path)
        text = extract_text(file_path)
        chunks = chunk_text(text)
        document_id = make_document_id(file_path)
        count = self.store.add_chunks(
            chunks=chunks,
            source=file_path.name,
            document_id=document_id,
        )
        return {
            "source": file_path.name,
            "document_id": document_id,
            "chunks_added": count,
        }

    def ask(self, question: str, top_k: int | None = None) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty")

        hits = self.store.search(
            question,
            top_k=top_k or self.config.default_top_k,
        )
        if not hits:
            return {
                "question": question,
                "answer": "I could not find any indexed documents to search.",
                "sources": [],
                "retrieved_passages": [],
                "generation_enabled": self.generator.enabled,
            }

        context_parts = []
        sources = []
        for index, hit in enumerate(hits, start=1):
            label = f"[{index}]"
            context_parts.append(
                f"{label} Source: {hit['source']} "
                f"(chunk {hit['chunk_index']})\n{hit['text']}"
            )
            sources.append(
                {
                    "citation": label,
                    "source": hit["source"],
                    "document_id": hit["document_id"],
                    "chunk_index": hit["chunk_index"],
                    "distance": hit["distance"],
                }
            )

        context = "\n\n".join(context_parts)
        answer = self.generator.generate(question, context)
        if answer is None:
            answer = (
                "Answer generation is not configured yet. The passages below "
                "are the retrieved evidence; configure an OpenAI-compatible "
                "LLM endpoint to generate a grounded answer."
            )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieved_passages": [
                {"citation": f"[{index}]", "text": hit["text"]}
                for index, hit in enumerate(hits, start=1)
            ],
            "generation_enabled": self.generator.enabled,
        }
