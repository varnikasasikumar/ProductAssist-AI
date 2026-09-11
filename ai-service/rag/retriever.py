from typing import List, Dict, Any, Optional
from .vector_store import get_vector_store, COLLECTION_NAME

def retrieve_knowledge_chunks(
    query: str,
    model: Optional[str] = None,
    top_k: int = 5,
    collection_name: str = COLLECTION_NAME
) -> List[Dict[str, Any]]:
    """
    Search ChromaDB for relevant knowledge chunks matching a natural language query.
    
    Args:
        query: User's natural language question or search phrase.
        model: Optional model identifier (e.g. 'CNC-X100') to filter metadata.
        top_k: Number of top results to retrieve (default: 5).
        collection_name: ChromaDB collection to search against.
        
    Returns:
        List of dicts formatted with content, metadata, and relevance distance scores.
    """
    collection = get_vector_store(collection_name)
    
    query_kwargs = {
        "query_texts": [query],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }
    
    # Apply metadata filtering if model is specified
    if model and model.strip():
        query_kwargs["where"] = {"model": model.strip()}

    raw_results = collection.query(**query_kwargs)

    formatted_results = []
    
    if raw_results and raw_results.get("documents") and len(raw_results["documents"]) > 0:
        documents = raw_results["documents"][0]
        metadatas = raw_results["metadatas"][0] if raw_results.get("metadatas") else []
        distances = raw_results["distances"][0] if raw_results.get("distances") else []

        for idx, text in enumerate(documents):
            meta = metadatas[idx] if idx < len(metadatas) else {}
            dist = distances[idx] if idx < len(distances) else None

            # Calculate a clean score (lower distance = higher similarity in L2 distance)
            score = round(float(dist), 4) if dist is not None else None

            item = {
                "content": text,
                "document_name": meta.get("document_name", ""),
                "document_type": meta.get("document_type", ""),
                "page_number": meta.get("page_number", 1),
                "section": meta.get("section", ""),
                "model": meta.get("model", ""),
                "product": meta.get("product", ""),
                "score": score,
                "source_file": meta.get("source_file", "")
            }
            formatted_results.append(item)

    return formatted_results
