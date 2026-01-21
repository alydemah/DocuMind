import tempfile
from pathlib import Path

import pytest

from app.rag.extractors.text import TextExtractor
from app.rag.extractors.markdown import MarkdownExtractor


class TestTextExtractor:
    def test_extract_text_file(self):
        extractor = TextExtractor()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello world\n\nThis is a test document.")
            f.flush()
            result = extractor.extract(Path(f.name))

        assert result.total_pages == 1
        assert len(result.pages) == 1
        assert "Hello world" in result.pages[0].content

    def test_extract_empty_file(self):
        extractor = TextExtractor()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            f.flush()
            result = extractor.extract(Path(f.name))

        assert result.total_pages == 1


class TestMarkdownExtractor:
    def test_extract_markdown(self):
        extractor = MarkdownExtractor()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Title\n\nSome content here.\n\n## Section 2\n\nMore content.")
            f.flush()
            result = extractor.extract(Path(f.name))

        assert result.total_pages == 1
        assert "Title" in result.pages[0].content
