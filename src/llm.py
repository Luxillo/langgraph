# src/llm.py
"""
Cliente LLM centralizado - soporta tanto Ollama local como Azure OpenAI.
"""

import os
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel


def get_llm() -> BaseChatModel:
    """
    Retorna el LLM configurado según las variables de entorno.
    Por defecto usa Qwen2.5:8B local via Ollama.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if llm_provider == "ollama":
        return get_ollama_llm()
    elif llm_provider == "azure":
        return get_azure_llm()
    else:
        raise ValueError(f"LLM_PROVIDER no soportado: {llm_provider}")


def get_ollama_llm() -> ChatOllama:
    """
    Retorna una instancia de ChatOllama para Qwen3:8B.
    """
    model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return ChatOllama(
        model=model,
        base_url=base_url,
        temperature=0.1,  # Más bajo para respuestas consistentes
    )


def get_azure_llm() -> AzureChatOpenAI:
    """
    Retorna una instancia configurada de AzureChatOpenAI.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    if not endpoint:
        raise RuntimeError("Falta AZURE_OPENAI_ENDPOINT. ¿Cargaste el .env?")
    if not api_key:
        raise RuntimeError("Falta AZURE_OPENAI_API_KEY. ¿Cargaste el .env?")
    if not deployment:
        raise RuntimeError("Falta AZURE_OPENAI_CHAT_DEPLOYMENT. ¿Cargaste el .env?")

    return AzureChatOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        azure_deployment=deployment,
        temperature=0.2,
    )