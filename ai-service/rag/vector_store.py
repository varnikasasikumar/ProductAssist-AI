import os
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

from .embeddings import get_embedding_function

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "product_knowledge"

def get_chroma_client(persist_dir: Path = None) -> chromadb.PersistentClient:
    """
    Get or create persistent ChromaDB client pointing to ai-service/chroma_db.
    """
    if persist_dir is None:
        persist_dir = CHROMA_DIR

    os.makedirs(persist_dir, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_dir))

def get_vector_store(collection_name: str = COLLECTION_NAME):
    """
    Retrieve or create the target ChromaDB collection for product knowledge.
    """
    client = get_chroma_client()
    embedding_fn = get_embedding_function()
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={"description": "RAG Knowledge Base for Product Operation, Troubleshooting, and Maintenance"}
    )
    return collection

def generate_deterministic_chunk_id(metadata: Dict[str, Any], chunk_index: int) -> str:
    """
    Generate stable, deterministic IDs to prevent duplicate chunk ingestion.
    Format: {model}_{doc_name}_p{page_number}_c{chunk_index}
    """
    model = metadata.get("model", "default").replace(" ", "_")
    doc_name = metadata.get("document_name", "unknown_doc").replace(".pdf", "").replace(".json", "")
    page_num = metadata.get("page_number", 1)
    return f"{model}_{doc_name}_p{page_num}_c{chunk_index}"


def upsert_chunks_to_vector_store(chunks: List[Dict[str, Any]], collection_name: str = COLLECTION_NAME) -> int:
    """
    Upserts (insert or update) text chunks with metadata into ChromaDB using deterministic IDs.
    
    Returns:
        int: Number of chunks upserted into ChromaDB.
    """
    if not chunks:
        return 0

    collection = get_vector_store(collection_name)

    documents = []
    metadatas = []
    ids = []

    for idx, chunk in enumerate(chunks):
        doc_text = chunk["text"]
        metadata = chunk["metadata"]
        
        # Ensure primitive string/int values for metadata compatibility
        clean_meta = {}
        for k, v in metadata.items():
            if isinstance(v, (str, int, float, bool)):
                clean_meta[k] = v
            else:
                clean_meta[k] = str(v)

        chunk_id = generate_deterministic_chunk_id(metadata, metadata.get("chunk_index", idx))

        documents.append(doc_text)
        metadatas.append(clean_meta)
        ids.append(chunk_id)

    # Upsert guarantees idempotent execution (no duplicate chunks created on re-run)
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return len(ids)

def query_vector_store(query_text: str, n_results: int = 5, collection_name: str = COLLECTION_NAME):
    """
    Perform semantic vector search against the ChromaDB product_knowledge collection.
    """
    collection = get_vector_store(collection_name)
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results
