"""Unit tests for document chunking and supported file types."""

import pytest

from rag_app.ingestion import chunk_text


def test_chunk_text_returns_one_chunk_for_short_text():
    assert chunk_text("one two three", chunk_size=5, overlap=1) == [
        "one two three"
    ]


def test_chunk_text_applies_overlap():
    assert chunk_text(
        "one two three four five six", chunk_size=4, overlap=1
    ) == ["one two three four", "four five six"]


def test_chunk_text_handles_empty_input():
    assert chunk_text("") == []


@pytest.mark.parametrize(
    ("chunk_size", "overlap"),
    [(0, 0), (4, -1), (4, 4), (4, 5)],
)
def test_chunk_text_rejects_invalid_parameters(chunk_size, overlap):
    with pytest.raises(ValueError):
        chunk_text("some words", chunk_size=chunk_size, overlap=overlap)
