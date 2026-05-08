import uuid
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from qdrant_client.models import PointStruct
from backend.app.rag.vectorstore import get_client, COLLECTION_NAME


def ingest_text_file(file_path: str) -> int:
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text",
                                  base_url="http://host.docker.internal:11434")
    texts = [chunk.page_content for chunk in chunks]
    vectors = embeddings.embed_documents(texts)

    client = get_client()

    points = []
    for text, vector in zip(texts, vectors):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": text}
        )
        points.append(point)
  

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)