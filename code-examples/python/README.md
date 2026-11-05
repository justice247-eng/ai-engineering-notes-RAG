# Python RAG Learning Project

This folder contains two practical exercises:

- `rag_local.py`: a small retrieval-only demo for learning embeddings and vector search.
- `rag_app/`: a modular document RAG application with PDF/TXT/Markdown ingestion, ChromaDB storage, source citations, a command-line interface, a FastAPI service, and optional LLM answer generation.

## Requirements

- Python 3.12 recommended.
- Internet access for the first download of the embedding model.
- No paid API key is required for ingestion or retrieval.
- Answer generation is optional and requires an OpenAI-compatible chat endpoint. A local Ollama endpoint can be used; hosted providers may charge for usage.

## Install

From the repository root, activate the virtual environment you created, then:

```bash
uv pip install -r code-examples/python/requirements.txt
```

Alternatively, use `python -m pip install -r code-examples/python/requirements.txt`.

## Run the retrieval-only lesson

```bash
cd code-examples/python
python rag_local.py
```

This first demo uses a few built-in passages. It retrieves similar text but does not generate an answer with an LLM.

## Run the full RAG application

Run these commands from `code-examples/python`:

```bash
python -m rag_app.cli ingest sample_docs
python -m rag_app.cli ask "What is retrieval-augmented generation?"
python -m rag_app.cli sources
python evaluate_retrieval.py
```

The first ingestion or query downloads the configured Sentence Transformers model if it is not already cached. The default model is `sentence-transformers/all-MiniLM-L6-v2`.

### Start the API

```bash
uvicorn rag_app.api:app --reload --host 0.0.0.0 --port 8000
```

Open the forwarded port 8000 in Codespaces. The interactive API documentation is available at `/docs`.

Endpoints:

- `GET /health` — service status.
- `POST /documents/upload` — upload a PDF, TXT, or Markdown file.
- `POST /query` — retrieve evidence and, when configured, generate an answer.
- `POST /agent/query` — let a bounded agent choose between the approved knowledge-base search and source-list tools.

Example query body:

```json
{
  "question": "What does chunk overlap do?",
  "top_k": 4
}
```

### Optional answer generation

Copy `.env.example` to `.env` and configure an OpenAI-compatible endpoint. For a local Ollama server that exposes its OpenAI-compatible API, an example configuration is:

```dotenv
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen2.5:3b
LLM_API_KEY=
```

The model must already be available to that Ollama server. In a cloud Codespace, `localhost` refers to the Codespace itself, not your personal computer. Do not assume a local Ollama server on your laptop is reachable from Codespaces.

For hosted providers, use their documented base URL and model name, add the API key only to your private `.env` or Codespaces secret, and check current pricing. Never commit real credentials.

If no generation endpoint is configured, the application still performs retrieval and returns the passages and source metadata. It does not pretend that a language model generated an answer.

## Configuration

Copy `.env.example` to `.env` in this folder to configure local settings. Keep real credentials in the private `.env` file or Codespaces secrets; never commit them.

| Variable | Purpose | Default |
|---|---|---|
| `RAG_DATA_DIR` | Local data directory | `./data` |
| `CHROMA_PATH` | Persistent Chroma database | `./data/chroma` |
| `CHROMA_COLLECTION` | Collection name | `rag_documents` |
| `EMBEDDING_MODEL` | Sentence Transformers model | `sentence-transformers/all-MiniLM-L6-v2` |
| `RAG_TOP_K` | Default number of retrieved chunks | `4` |
| `MAX_UPLOAD_MB` | Maximum upload size | `15` |
| `LLM_BASE_URL` | OpenAI-compatible API base URL | unset |
| `LLM_MODEL` | Chat model name | unset |
| `LLM_API_KEY` | Optional provider key | unset |

## Run tests

From `code-examples/python`:

```bash
python -m pytest -q
```

## Important limitations

- The initial PDF extractor reads embedded text. Scanned image-only PDFs need OCR, which is not included yet.
- The default chunker is deliberately simple and word-based. Production systems should evaluate chunking against their document types and question set.
- Similarity search returns candidates, not proof. Review citations and evaluate answer quality.
- This learning API is not production-hardened. Add authentication, per-user document isolation, rate limits, malware scanning, stronger upload controls, observability, and deployment-specific secret management before exposing it publicly.
