import os
import sys

# Ensure local module import works
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rag.answer_generator import generate_grounded_answer

queries = [
    "What is the maximum spindle speed of the CNC-X100?",
    "What are the X Y and Z axis travels?",
    "What pneumatic pressure does the CNC-X100 require?",
    "What are the electrical requirements?",
    "What are the daily maintenance checks?",
    "When should the coolant be replaced?",
    "What does E105 mean?",
    "What does E210 mean?",
    "What does E315 mean?",
    "What does E420 mean?",
    "What communication protocols does the CNC-X100 support?",
    "What PPE is required?",
    "What is the operating temperature range?",
    "What should I check before starting the machine?",
    "What maintenance was recently performed?"
]

print("=" * 80)
print("             PRODUCTASSIST AI - 15 GROUNDED RAG QUERY AUDIT")
print("=" * 80)

for idx, q in enumerate(queries, start=1):
    res = generate_grounded_answer(query=q, model="CNC-X100")
    doc_sources = [f"{s['document_name']} (Page {s['page_number']})" for s in res['sources']]
    print(f"\nQ{idx}: '{q}'")
    print(f"  Sources ({len(doc_sources)}): {doc_sources[:3]}")
    print(f"  Answer:\n  {res['answer'][:250]}...\n")
    print("-" * 80)

print("\nAll 15 Grounded RAG Queries Executed Successfully!")
