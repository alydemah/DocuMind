from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.config import settings


class VectorStore:
    def __init__(self, host: str, port: int, collection_name: str):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

    def ensure_collection(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.embedding_dimensions,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_vectors(
        self,
        ids: list[str],
        vectors: list[list[float]],
        payloads: list[dict],
    ):
        self.ensure_collection()
        points = [
            PointStruct(id=id_, vector=vector, payload=payload)
            for id_, vector, payload in zip(ids, vectors, payloads)
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        score_threshold: float = 0.7,
        document_filter: list[str] | None = None,
    ) -> list[dict]:
        self.ensure_collection()

        query_filter = None
        if document_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=doc_id),
                    )
                    for doc_id in document_filter
                ]
            )

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            query_filter=query_filter,
        )

        return [
            {
                "id": str(hit.id),
                "score": hit.score,
                "document_id": hit.payload.get("document_id", ""),
                "document_name": hit.payload.get("document_name", ""),
                "chunk_index": hit.payload.get("chunk_index", 0),
                "page_number": hit.payload.get("page_number"),
                "content": hit.payload.get("content", ""),
            }
            for hit in results
        ]

    def delete_by_document(self, document_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )

    def count(self) -> int:
        try:
            info = self.client.get_collection(self.collection_name)
            return info.points_count or 0
        except Exception:
            return 0
