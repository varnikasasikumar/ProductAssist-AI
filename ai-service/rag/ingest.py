import sys
from pathlib import Path

from .document_loader import load_pdf_documents, find_knowledge_base_dir
from .chunker import chunk_documents
from .vector_store import upsert_chunks_to_vector_store, query_vector_store, get_vector_store

def run_ingestion():
    """Run the RAG knowledge base ingestion pipeline."""
    print("=" * 70)
    print("      PRODUCTASSIST AI - RAG KNOWLEDGE BASE INGESTION PIPELINE")
    print("=" * 70)

    # Load documents
    kb_dir = find_knowledge_base_dir()
    print(f"\n[1/4] Loading PDF documents from: {kb_dir}")
    doc_pages = load_pdf_documents(kb_dir)
    
    unique_docs = set(p["metadata"]["document_name"] for p in doc_pages)
    total_pages = len(doc_pages)
    
    print(f"      -> Found {len(unique_docs)} documents ({', '.join(sorted(list(unique_docs)))})")
    print(f"      -> Extracted {total_pages} total pages page-by-page.")

    # Chunk documents
    print("\n[2/4] Performing structure-aware recursive chunking...")
    chunks = chunk_documents(doc_pages)
    print(f"      -> Created {len(chunks)} text chunks.")

    # Store embeddings in ChromaDB
    print("\n[3/4] Generating embeddings and persisting to ChromaDB...")
    num_stored = upsert_chunks_to_vector_store(chunks)
    print(f"      -> Stored {num_stored} chunks in ChromaDB collection 'product_knowledge'.")

    # Verify collection count
    collection = get_vector_store()
    collection_count = collection.count()
    print(f"      -> Total persisted documents in collection: {collection_count}")

    # Verify retrieval
    print("\n[4/4] Verifying vector retrieval for synthetic error codes...")
    print("-" * 70)
    
    test_queries = ["E105", "E210", "E315", "E420"]
    for q in test_queries:
        res = query_vector_store(q, n_results=1)
        if res and res["documents"] and res["documents"][0]:
            chunk_txt = res["documents"][0][0][:180].replace("\n", " ")
            meta = res["metadatas"][0][0]
            print(f"  [QUERY: '{q}']")
            print(f"    - Document : {meta.get('document_name')} (Page {meta.get('page_number')})")
            print(f"    - Type     : {meta.get('document_type')}")
            print(f"    - Section  : {meta.get('section')}")
            print(f"    - Snippet  : {chunk_txt}...")
            print("-" * 70)

    print("\nRAG Ingestion Pipeline completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    run_ingestion()
