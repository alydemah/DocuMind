from dataclasses import dataclass

import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import settings


@dataclass
class Chunk:
    content: str
    chunk_index: int
    page_number: int | None
    token_count: int
    metadata: dict


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.chunk_size = chunk_size or settings.rag_chunk_size
        self.chunk_overlap = chunk_overlap or settings.rag_chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " "],
            length_function=self._token_length,
        )

    def _token_length(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def chunk_text(
        self,
        text: str,
        document_id: str,
        document_name: str,
        page_number: int | None = None,
    ) -> list[Chunk]:
        splits = self.splitter.split_text(text)
        chunks = []

        for i, content in enumerate(splits):
            token_count = self._token_length(content)
            chunks.append(
                Chunk(
                    content=content,
                    chunk_index=i,
                    page_number=page_number,
                    token_count=token_count,
                    metadata={
                        "document_id": document_id,
                        "document_name": document_name,
                        "chunk_index": i,
                        "page_number": page_number,
                        "total_chunks": len(splits),
                    },
                )
            )

        return chunks

    def chunk_pages(
        self,
        pages: list[dict],
        document_id: str,
        document_name: str,
    ) -> list[Chunk]:
        all_chunks: list[Chunk] = []
        global_index = 0

        for page in pages:
            page_chunks = self.chunk_text(
                text=page["content"],
                document_id=document_id,
                document_name=document_name,
                page_number=page.get("page_number"),
            )

            for chunk in page_chunks:
                chunk.chunk_index = global_index
                chunk.metadata["chunk_index"] = global_index
                global_index += 1

            all_chunks.extend(page_chunks)

        for chunk in all_chunks:
            chunk.metadata["total_chunks"] = len(all_chunks)

        return all_chunks
