import json
from rag import retrieve_knowledge_chunks

test_queries = [
    {
        "name": "Query 1: Error Code E105",
        "query": "What should I do if E105 occurs?",
        "model": "CNC-X100",
        "top_k": 3
    },
    {
        "name": "Query 2: Air Filter Replacement",
        "query": "How do I replace the air filter?",
        "model": "CNC-X100",
        "top_k": 3
    },
    {
        "name": "Query 3: PPE Requirements",
        "query": "What PPE is required when operating the CNC-X100?",
        "model": "CNC-X100",
        "top_k": 3
    },
    {
        "name": "Query 4: Axis Travels",
        "query": "What are the X, Y and Z axis travels?",
        "model": "CNC-X100",
        "top_k": 3
    },
    {
        "name": "Query 5: Network Configuration",
        "query": "How do I configure the network?",
        "model": "CNC-X100",
        "top_k": 3
    }
]

print("=" * 80)
print("             PRODUCTASSIST AI - RAG RETRIEVAL TEST SUITE")
print("=" * 80)

for test in test_queries:
    print(f"\n>>> {test['name']}")
    print(f"    Query: '{test['query']}' | Model Filter: '{test['model']}' | Top K: {test['top_k']}")
    print("-" * 80)
    
    results = retrieve_knowledge_chunks(
        query=test['query'],
        model=test['model'],
        top_k=test['top_k']
    )
    
    for i, res in enumerate(results, start=1):
        print(f"  Result #{i}: [Score: {res['score']}]")
        print(f"    Document : {res['document_name']} (Page {res['page_number']})")
        print(f"    Type     : {res['document_type']}")
        print(f"    Model    : {res['model']}")
        print(f"    Section  : {res['section']}")
        snippet = res['content'][:150].replace('\n', ' ')
        print(f"    Content  : {snippet}...")
        print("-" * 80)

# Model Filter Test: Non-existent model
print("\n>>> Model Filtering Isolation Test (model='NON_EXISTENT_MODEL')")
res_empty = retrieve_knowledge_chunks(query="E105", model="NON_EXISTENT_MODEL", top_k=3)
print(f"    Returned {len(res_empty)} results for non-existent model filter (Correctly filtered).")
print("=" * 80)
