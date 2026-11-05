# 3. RAG Architecture and Data Flow

## Main components
| Component | Responsibility |
|---|---|
| User interface | Accepts questions and displays answers |
| Backend API | Authenticates, validates and orchestrates |
| Ingestion pipeline | Extracts, cleans and chunks documents |
| Embedding model | Converts text into vectors |
| Search database | Finds candidate passages |
| Metadata store | Holds source, page and permission data |
| Retriever | Selects candidate passages |
| Reranker | Reorders candidates by relevance |
| LLM | Generates a readable answer |
| Observability | Measures errors, latency, quality and cost |

## Architecture diagram

    DOCUMENT INGESTION
    Files → Extract text → Clean → Chunk → Embedding model
                                            ↓
                                    Vector/search index

    USER QUESTION
    User → UI → Backend → Authentication → Retriever
                                            ↓
                                         Reranker
                                            ↓
                                      Context builder
                                            ↓
                                          LLM
                                            ↓
                                  Answer + source references

## Separate ingestion from question answering
Ingestion is a background or upload-triggered process. It tracks versions, handles duplicates, indexes content and records failures.

The query pipeline runs for each question. It authenticates the user, enforces permissions, retrieves evidence, builds bounded context and generates a response.

## Metadata and multi-tenancy
A chunk may carry document_id, chunk_id, tenant_id, access_groups, source, page and version. The backend must derive permitted scope from the authenticated identity. Do not trust a filter supplied by the browser as the security boundary.

## Reliability
- If embedding fails, return a controlled error.
- If no useful evidence is found, say so or ask a clarifying question.
- If sources conflict, expose the conflict or use a documented priority rule.
- If a document is deleted, remove or invalidate its chunks and caches.
- Use bounded retries and timeouts.

## Exercise
Design a school-notes assistant. Identify where login occurs, how course access is checked, how page citations are preserved and how cross-student retrieval is prevented.