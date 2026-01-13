from app.rag.extractors.base import BaseExtractor
from app.rag.extractors.pdf import PDFExtractor
from app.rag.extractors.docx import DocxExtractor
from app.rag.extractors.text import TextExtractor
from app.rag.extractors.markdown import MarkdownExtractor

EXTRACTORS: dict[str, type[BaseExtractor]] = {
    "pdf": PDFExtractor,
    "docx": DocxExtractor,
    "txt": TextExtractor,
    "md": MarkdownExtractor,
}


def get_extractor(file_type: str) -> BaseExtractor:
    extractor_class = EXTRACTORS.get(file_type)
    if not extractor_class:
        raise ValueError(f"Unsupported file type: {file_type}")
    return extractor_class()


__all__ = [
    "BaseExtractor",
    "PDFExtractor",
    "DocxExtractor",
    "TextExtractor",
    "MarkdownExtractor",
    "get_extractor",
]
