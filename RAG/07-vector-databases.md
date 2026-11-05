# 7. Vector Databases

A vector database stores embedding vectors and supports nearest-neighbour search. Many systems also store text, metadata and filters.

## Tools to investigate
| Tool | Typical use | Notes |
|---|---|---|
| FAISS | Local vector similarity | Library; metadata and persistence may need separate handling |
| Chroma | Local prototyping and vector storage | Convenient developer workflow |
| PostgreSQL + pgvector | Relational data plus vector search | Useful when application data already lives in PostgreSQL |
| Qdrant | Vector search engine | Open-source core and hosted options |
| Weaviate | Vector database and search platform | Supports vector and hybrid patterns |
| Pinecone | Managed vector database | Hosted service; check pricing and limits |
| Elasticsearch / OpenSearch | Search with vector capabilities | Useful when lexical search is also important |

These are options, not rankings. Verify current features, licensing, pricing and deployment requirements.

## Selection checklist
1. Does it support your vector dimensions and metric?
2. Can it filter metadata securely?
3. Does it support hybrid search?
4. Can you persist and back up data?
5. What are the usage limits and costs?
6. Can you run it locally?
7. How do you update and delete a document's chunks?
8. Does it meet privacy requirements?

A vector database does not automatically extract PDFs, choose good chunk boundaries, enforce all application permissions, validate citations or generate reliable answers. Those belong to the wider RAG system.

## Exercise
Compare Chroma, FAISS and PostgreSQL with pgvector for a student-notes assistant. Record setup difficulty, persistence, filtering, local operation and cost.