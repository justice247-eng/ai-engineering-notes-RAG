# 5. Embeddings and Semantic Search

## What is an embedding?
An embedding model converts text into a vector: a list of floating-point numbers. Sentences with similar meanings may be represented by vectors that are close under a similarity metric.

Example:
- "How do I reset my password?"
- "I forgot my login password. How can I change it?"

A semantic model may recognise their similar meaning even though the words differ. An embedding is not a human-readable summary.

## Similarity
Cosine similarity compares the angle between vectors:

    cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

Other common metrics include dot product and Euclidean distance. Follow the embedding model and database recommendations.

## Keyword versus semantic search
Question: "How can I get my money back?"
- Keyword search looks for terms such as money and back.
- Semantic search may find a section titled "Refund policy".
- Hybrid search combines both and can be useful for exact names and broader meaning.

Similarity does not automatically mean factual relevance.

## Toy Python example
This uses invented vectors to demonstrate cosine similarity. These are NOT real language embeddings.

    def cosine_similarity(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    password_help = [0.8, 0.1, 0.2]
    reset_login = [0.75, 0.12, 0.18]
    banana_bread = [0.05, 0.9, 0.7]

    print(cosine_similarity(password_help, reset_login))
    print(cosine_similarity(password_help, banana_bread))

## Choosing an embedding model
Evaluate language support, retrieval quality on your own questions, vector dimensions, latency, throughput, cost, licensing, privacy and local-running options.

Use compatible embedding models and dimensions for indexed chunks and incoming queries. Changing the model usually means re-embedding the collection.

## Exercise
Write five differently worded questions that should retrieve the same paragraph from a course handbook. Explain why exact keyword search may miss some.