#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Project environment not found. Run: bash scripts/setup_rag.sh"
  exit 1
fi

source .venv/bin/activate
cd code-examples/python

python -m rag_app.cli ingest sample_docs
echo
python -m rag_app.cli ask "What is retrieval-augmented generation?"
