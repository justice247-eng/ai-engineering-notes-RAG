# RAG Production Readiness and Security Checklist

A working demo is not automatically safe or reliable for real users.

## Identity and access control

- Authenticate every user.
- Authorize every document read, search, update and delete.
- Enforce tenant filters server-side.
- Test that one user cannot retrieve another user's content.
- Avoid treating document IDs or obscure URLs as access controls.

## Data protection

- Use HTTPS in deployment.
- Keep API keys in a secret manager or private environment variables.
- Never commit `.env`, credentials, tokens or private documents.
- Define retention and deletion policies.
- Encrypt sensitive data at rest where appropriate.
- Restrict access to backups and vector database files.

## Ingestion safety

- Allow only required file types.
- Enforce file-size and page-count limits.
- Treat file extensions and MIME types as untrusted.
- Consider malware scanning and sandboxed parsing.
- Handle malformed files and parser timeouts.
- Prevent path traversal and unsafe filenames.
- Consider OCR and parser quality checks for scanned or complex documents.

## Retrieval and generation

- Filter by authorization before retrieval.
- Track source and document versions.
- Treat retrieved passages as untrusted context.
- Defend against indirect prompt injection.
- Require citations and test citation correctness.
- Provide a clear no-evidence response.
- Evaluate retrieval quality and answer faithfulness.
- Do not let a model execute arbitrary tools or SQL.

## Reliability and operations

- Set request timeouts and bounded retries.
- Rate-limit uploads and queries.
- Monitor latency, errors, token use and storage.
- Track embedding model and index versions.
- Back up and test restoring the vector store.
- Re-index safely when models or chunking strategies change.
- Add health checks and alerts.
- Load-test realistic document and query sizes.

## Before public launch

The learning API in this repository is intentionally not production-hardened. It does not yet provide authentication, multi-tenant authorization, malware scanning, OCR, a managed secrets service, production observability or a deployment configuration.

Do not expose it publicly with private documents until these controls have been implemented and reviewed.
