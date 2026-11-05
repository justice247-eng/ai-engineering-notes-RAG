# 2. How RAG Works

A typical RAG system has two main phases: indexing and retrieval-generation.

## Phase A: Indexing
1. Collect sources: PDFs, DOCX, websites, Markdown or approved APIs.
2. Extract text. Scanned PDFs may require OCR.
3. Clean and normalise the text.
4. Split long documents into chunks.
5. Create embeddings for each chunk.
6. Store vectors, text and metadata in a search index.

    Documents → Extract → Clean → Chunk → Embed → Vector index
                                             ↘ Text and metadata store

Indexing is usually done when documents are uploaded or updated, not every time someone asks a question.

## Phase B: Retrieval and generation
1. User asks a question.
2. Convert the question into an embedding for dense retrieval.
3. Search for relevant chunks.
4. Optionally rerank the candidates.
5. Assemble a prompt with the question and selected evidence.
6. Ask the LLM to generate an answer.
7. Return the answer and source references.

    Question → Query embedding → Retrieve → Rerank → Context
                                                    ↓
    Answer with sources ← Validate ← LLM generation

## Simple example
Source passage: "The visitor centre opens Tuesday to Sunday, 9 a.m. to 5 p.m. It is closed on Mondays."

Question: "Can I visit on Monday?"

Retrieved evidence: the passage above.

Grounded answer: "No. The visitor centre is closed on Mondays."

## What a chunk record can contain
- Unique chunk ID and parent document ID.
- Text content and embedding vector.
- Source filename or canonical URL.
- Page number and section heading.
- Version and update timestamp.
- Tenant and access-group metadata where required.

## Important design decisions
- Are sources trusted and current?
- How are updates and deletions handled?
- How large should chunks be?
- Which embedding model supports the data's languages?
- Should search be lexical, vector or hybrid?
- How many candidates should be retrieved?
- How are citations validated?
- What happens when evidence is insufficient?

## Exercise
Draw the two phases for a chatbot that answers from bootcamp PDF notes. Show where page numbers are preserved and where the LLM receives retrieved text.