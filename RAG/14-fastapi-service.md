# Exposing a RAG Pipeline Through an API

An API lets a website, mobile application or another service use your RAG pipeline without importing its Python code directly.

## 1. Why FastAPI?

[FastAPI](https://fastapi.tiangolo.com/) is a Python framework for building HTTP APIs. It provides request validation, generated OpenAPI documentation and asynchronous request support.

## 2. Project endpoints

The learning app exposes:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check whether the service is responding |
| POST | `/documents/upload` | Upload a PDF, TXT or Markdown file for indexing |
| POST | `/query` | Retrieve evidence and optionally generate an answer |

Interactive API documentation is available at `/docs` while the local server is running.

## 3. Start the API

From `code-examples/python`:

```bash
uvicorn rag_app.api:app --reload --host 0.0.0.0 --port 8000
```

In Codespaces, open the forwarded port 8000 using the Ports panel.

## 4. Example query

Send a POST request to `/query` with:

```json
{
  "question": "What is an embedding?",
  "top_k": 4
}
```

The response includes an answer field, retrieved passages and source metadata. If no generation endpoint is configured, the answer field explains that only retrieval was performed.

## 5. Security considerations

The starter API is for learning and local testing. Before public deployment, add:

- authentication and authorization;
- per-user or per-organization document isolation;
- request and upload rate limits;
- upload scanning and stricter content validation;
- secure secret management;
- HTTPS and appropriate CORS settings;
- deletion and retention controls;
- monitoring and structured logs.

Never assume that hiding a document identifier makes a document private. Enforce access control on every retrieval request.
