from langchain_ollama import ChatOllama, OllamaEmbeddings

from backend.app.core.cache import get_cache, set_cache
from backend.app.core.config import settings
from backend.app.rag.vectorstore import get_client, COLLECTION_NAME


def retrieve_context(question: str, top_k: int = 3) -> str:
    embeddings = OllamaEmbeddings(model=settings.ollama_embed_model,
                                  base_url="http://host.docker.internal:11434")
    client = get_client()

    query_vector = embeddings.embed_query(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    ).points

    contexts = [
        res.payload.get("text", "")
        for res in results
        if res.payload and res.payload.get("text")
    ]

    return "\n\n".join(contexts)


def generate_answer(question: str) -> str:
    cached = get_cache(question)
    if cached:
        return cached

    context = retrieve_context(question)

    if not context.strip():
        return "I don't know based on the provided documents."

    context = context[:1500]

    llm = ChatOllama(
        model=settings.ollama_llm_model,
        temperature=0,
        base_url="http://host.docker.internal:11434"
    )

    prompt = f"""
You are a helpful and accurate assistant.

Rules:
- Answer ONLY using the provided context.
- Do NOT use external knowledge.
- If the answer is not clearly in the context, say: "I don't know based on the provided documents."
- Keep the answer clear, concise, and well-structured.
- If possible, summarize instead of copying.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    answer = response.content

    set_cache(question, answer)

    return answer