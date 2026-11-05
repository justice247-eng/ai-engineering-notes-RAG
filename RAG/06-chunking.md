# Chunking

Chunking divides documents into passages for indexing and retrieval. Strategies include fixed-size, overlapping, sentence, paragraph, structure-aware and semantic chunking.

Preserve source filename, document ID, page, section, version and access labels. Scanned PDFs may need OCR; tables and code need structure-aware extraction.

There is no universal chunk size. Evaluate with representative questions: did retrieval find the right passage, does it contain enough context, are duplicates excessive, and how many tokens are sent to the model?

Example: with a 500-token chunk and 50-token overlap, the next chunk begins 450 tokens after the previous chunk's start.