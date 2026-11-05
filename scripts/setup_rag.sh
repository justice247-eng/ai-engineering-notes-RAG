#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# uv is installed in the Codespaces user's local bin directory.
export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv was not found. Install it from https://docs.astral.sh/uv/ first."
  exit 1
fi

if [[ ! -x ".venv/bin/python" ]]; then
  uv venv --python 3.12
fi

source .venv/bin/activate
uv pip install -r code-examples/python/requirements.txt

echo
echo "RAG dependencies installed."
echo "Running the lightweight unit tests..."
python -m pytest -q code-examples/python/tests

echo
echo "Setup and tests finished."
echo "Next: cd code-examples/python"
echo 'Then: python -m rag_app.cli ingest sample_docs'
