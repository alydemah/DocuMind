from pathlib import Path

from app.rag.extractors.base import BaseExtractor, ExtractedPage, ExtractionResult


class MarkdownExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> ExtractionResult:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        cleaned = self._clean_text(content)

        pages = [
            ExtractedPage(
                page_number=1,
                content=cleaned,
                metadata={"format": "markdown"},
            )
        ]

        return ExtractionResult(
            pages=pages,
            total_pages=1,
            metadata={"format": "markdown", "char_count": len(content)},
        )
