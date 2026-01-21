import pytest
from app.rag.chunker import DocumentChunker


class TestDocumentChunker:
    def test_chunk_text_basic(self):
        chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
        text = "This is a test paragraph. " * 20
        chunks = chunker.chunk_text(
            text=text,
            document_id="test-id",
            document_name="test.txt",
        )
        assert len(chunks) > 0
        assert chunks[0].chunk_index == 0
        assert chunks[0].metadata["document_id"] == "test-id"

    def test_chunk_text_short(self):
        chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
        text = "Short text."
        chunks = chunker.chunk_text(
            text=text,
            document_id="test-id",
            document_name="test.txt",
        )
        assert len(chunks) == 1
        assert chunks[0].content == "Short text."

    def test_chunk_pages(self):
        chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
        pages = [
            {"content": "First page content. " * 15, "page_number": 1},
            {"content": "Second page content. " * 15, "page_number": 2},
        ]
        chunks = chunker.chunk_pages(
            pages=pages,
            document_id="test-id",
            document_name="test.pdf",
        )
        assert len(chunks) > 2
        assert chunks[-1].chunk_index == len(chunks) - 1
