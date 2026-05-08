from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from backend.app.core.config import settings


COLLECTION_NAME = settings.collection_name

client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key or None
)


def create_collection():
    existing_collections = client.get_collections().collections
    existing_names = [collection.name for collection in existing_collections]

    if COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )


def get_client():
    return client