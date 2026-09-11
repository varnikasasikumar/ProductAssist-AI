"""
ProductAssist AI - RAG Knowledge Base Package
"""

from .document_loader import load_pdf_documents
from .chunker import chunk_documents
from .embeddings import get_embedding_function
from .vector_store import get_vector_store, upsert_chunks_to_vector_store
from .retriever import retrieve_knowledge_chunks
from .llm import LLMClient, LLMKeyMissingError, LLMProviderError
from .answer_generator import generate_grounded_answer

__all__ = [
    "load_pdf_documents",
    "chunk_documents",
    "get_embedding_function",
    "get_vector_store",
    "upsert_chunks_to_vector_store",
    "retrieve_knowledge_chunks",
    "LLMClient",
    "LLMKeyMissingError",
    "LLMProviderError",
    "generate_grounded_answer",
]
