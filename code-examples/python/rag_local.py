from sentence_transformers import SentenceTransformer
import chromadb

# Small, invented knowledge collection for learning.
DOCUMENTS = [
    {
        "id": "tourism-1",
        "source": "tourism-notes.txt",
        "text": "Tourism is the temporary movement of people outside their usual environment for leisure, business or other purposes."
    },
    {
        "id": "tourism-2",
        "source": "tourism-notes.txt",
        "text": "The tourism product can include transport, accommodation, attractions, food services and visitor experiences."
    },
    {
        "id": "hospitality-1",
        "source": "hospitality-notes.txt",
        "text": "Hospitality focuses on welcoming guests and providing services such as accommodation, food and beverages."
    },
    {
        "id": "rag-1",
        "source": "ai-notes.txt",
        "text": "Retrieval-augmented generation retrieves relevant passages and supplies them to a language model as context."
    },
]


def simple_chunks(text: str, words_per_chunk: int = 35, overlap: int = 5):
    """A deliberately simple word-based chunker for a first exercise."""
    words = text.split()
    if words_per_chunk <= 0 or overlap < 0 or overlap >= words_per_chunk:
        raise ValueError("Use words_per_chunk > overlap >= 0")

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + words_per_chunk, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def main():
    # This model runs locally after its initial download.
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="./chroma_data")
    collection = client.get_or_create_collection(
        name="beginner_rag_notes",
        metadata={"hnsw:space": "cosine"}
    )

    ids, texts, metadatas = [], [], []
    for document in DOCUMENTS:
        for index, chunk in enumerate(simple_chunks(document["text"])):
            ids.append(f'{document["id"]}-chunk-{index}')
            texts.append(chunk)
            metadatas.append({
                "source": document["source"],
                "document_id": document["id"],
                "chunk_number": index
            })

    # Rebuild this demo collection on each run so changes to sample data are reflected.
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    vectors = embedding_model.encode(texts, normalize_embeddings=True).tolist()
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=vectors
    )

    question = input("Ask a question about the sample notes: ").strip()
    if not question:
        print("Please enter a question.")
        return

    query_vector = embedding_model.encode(
        [question],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_vector,
        n_results=min(3, len(texts)),
        include=["documents", "metadatas", "distances"]
    )

    print("\nRetrieved passages (not yet an LLM-generated answer):")
    for rank, (document, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ), start=1):
        print(f"\n{rank}. Source: {metadata['source']}")
        print(f"   Distance: {distance:.4f} (lower is closer for this metric)")
        print(f"   Passage: {document}")

    print("\nRemember: nearest-neighbour results are candidates, not proof that the question was answered.")


if __name__ == "__main__":
    main()
