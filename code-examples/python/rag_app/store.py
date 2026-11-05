"""Local embedding generation and Chroma vector storage."""

import chromadb
from sentence_transformers import SentenceTransformer

from .config import Settings


class VectorStore:
    def __init__(self, config: Settings):
        config.chroma_path.mkdir(parents=True, exist_ok=True)
        self.embedding_model = SentenceTransformer(config.embedding_model)
        self.client = chromadb.PersistentClient(path=str(config.chroma_path))
        self.collection = self.client.get_or_create_collection(
            name=config.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[str],
        source: str,
        document_id: str,
    ) -> int:
        if not chunks:
            return 0

        ids = [f"{document_id}-{index}" for index in range(len(chunks))]
        metadatas = [
            {
                "source": source,
                "document_id": document_id,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]
        vectors = self.embedding_model.encode(
            chunks, normalize_embeddings=True
        ).tolist()

        # upsert makes re-ingesting the same document idempotent.
        self.collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
            embeddings=vectors,
        )
        return len(chunks)

    def search(self, question: str, top_k: int = 4) -> list[dict]:
        if not question.strip():
            raise ValueError("Question cannot be empty")
        if top_k < 1 or top_k > 20:
            raise ValueError("top_k must be between 1 and 20")
        if self.collection.count() == 0:
            return []

        query_vector = self.embedding_model.encode(
            [question], normalize_embeddings=True
        ).tolist()
        result = self.collection.query(
            query_embeddings=query_vector,
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        hits = []
        for document, metadata, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        ):
            hits.append(
                {
                    "text": document,
                    "source": metadata.get("source", "unknown"),
                    "document_id": metadata.get("document_id", ""),
                    "chunk_index": metadata.get("chunk_index", -1),
                    "distance": float(distance),
                }
            )
        return hits

    def list_sources(self) -> list[str]:
        records = self.collection.get(include=["metadatas"])
        return sorted(
            {
                metadata.get("source", "unknown")
                for metadata in records["metadatas"]
                if metadata
            }
        )
