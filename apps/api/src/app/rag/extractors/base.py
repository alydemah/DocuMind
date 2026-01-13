from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ExtractedPage:
    page_number: int
    content: str
    metadata: dict = field(default_factory=dict)


@dataclass
class ExtractionResult:
    pages: list[ExtractedPage]
    total_pages: int
    metadata: dict = field(default_factory=dict)

    @property
    def full_text(self) -> str:
        return "\n\n".join(page.content for page in self.pages)


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractionResult:
        pass

    def _clean_text(self, text: str) -> str:
        lines = text.split("\n")
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                cleaned.append(stripped)
            elif cleaned and cleaned[-1] != "":
                cleaned.append("")
        return "\n".join(cleaned).strip()
