from pathlib import Path

import fitz

from app.rag.extractors.base import BaseExtractor, ExtractedPage, ExtractionResult


class PDFExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> ExtractionResult:
        doc = fitz.open(str(file_path))
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            cleaned = self._clean_text(text)

            if cleaned:
                pages.append(
                    ExtractedPage(
                        page_number=page_num + 1,
                        content=cleaned,
                        metadata={"width": page.rect.width, "height": page.rect.height},
                    )
                )

        total_pages = len(doc)
        doc.close()

        return ExtractionResult(
            pages=pages,
            total_pages=total_pages,
            metadata={"format": "pdf"},
        )
