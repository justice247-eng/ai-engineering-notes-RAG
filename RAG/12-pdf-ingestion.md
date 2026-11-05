# PDF and Document Ingestion

Document ingestion is the process of turning source files into text and metadata that a RAG system can search.

## 1. The ingestion pipeline

```text
PDF / TXT / Markdown
        |
        v
File validation
        |
        v
Text extraction
        |
        v
Cleaning and normalization
        |
        v
Chunking
        |
        v
Embedding generation
        |
        v
Vector database + metadata
```

## 2. Text extraction

For text-based PDFs, a library such as [pypdf](https://pypi.org/project/pypdf/) can extract embedded text page by page.

Extraction is not the same as OCR:

- Text-based PDF: characters are stored in the document and can usually be extracted.
- Scanned PDF: pages are images. An OCR engine must recognize the characters first.
- Complex PDF: tables, columns, headers and footnotes may be extracted in the wrong order.

Always inspect extracted text before indexing important documents. Poor extraction creates poor retrieval.

## 3. Cleaning

Typical safe cleanup includes normalizing whitespace, removing repeated blank lines and preserving paragraph boundaries. Do not remove meaningful headings, table labels, units, dates or page references just to make text shorter.

## 4. Chunking

A chunk is a smaller passage indexed separately. The starter app uses a simple word-based chunker with overlap.

Example with a chunk size of 5 words and overlap of 2:

- Chunk 1: `RAG retrieves relevant passages from`
- Chunk 2: `passages from documents for a question`

Overlap helps preserve meaning around boundaries. It also increases storage and duplicate retrieval, so tune it rather than choosing a large overlap automatically.

## 5. Metadata

Store useful metadata beside every chunk:

- original source filename;
- stable document identifier;
- chunk index;
- page number, when available;
- tenant or access-control identifier in multi-user systems;
- ingestion timestamp and document version.

Metadata is essential for citations, filtering, deletion and access control.

## 6. Current project exercise

From `code-examples/python`, run:

```bash
python -m rag_app.cli ingest sample_docs
python -m rag_app.cli sources
```

Then ask:

```bash
python -m rag_app.cli ask "Why does chunk overlap matter?"
```

The first run downloads the embedding model if it is not already cached.

## 7. Important limitations

The starter app extracts embedded PDF text but does not include OCR. It uses word-based chunking and does not yet preserve page-level citations. These are deliberate learning boundaries, not guarantees that all PDFs will be parsed perfectly.

## Further reading

- [pypdf documentation](https://pypdf.readthedocs.io/)
- [Unstructured documentation](https://docs.unstructured.io/)
