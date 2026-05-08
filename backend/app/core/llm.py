from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm():

    # 🔥 Local development mode
    if settings.llm_provider == "ollama":
        return ChatOllama(
            model=settings.ollama_llm_model,
            temperature=0,
            base_url=settings.ollama_base_url
        )

    # 🔥 Production cloud mode
    elif settings.llm_provider == "openai":
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0
        )

    else:
        raise ValueError("Unsupported LLM provider")