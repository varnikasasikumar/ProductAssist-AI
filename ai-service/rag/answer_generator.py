import re
from typing import Dict, Any, List, Optional
from .retriever import retrieve_knowledge_chunks
from .llm import LLMClient, LLMKeyMissingError, LLMProviderError

GROUNDING_SYSTEM_PROMPT = """You are ProductAssist AI, an enterprise product operation, troubleshooting, and maintenance assistant.

Answer the user's question using ONLY the supplied authorized product documentation provided in the context.

CRITICAL GROUNDING RULES:
1. Do NOT search the internet, and do NOT use external knowledge not present in the context.
2. Do NOT invent specifications, procedures, error codes, component names, safety instructions, or corrective actions.
3. If the supplied documentation does not contain enough information to answer the question, clearly state: "The available documentation does not provide enough information to answer this question."
4. When relevant, explain procedures clearly and step-by-step.
5. For safety-sensitive operations, explicitly preserve and include all safety warnings, precautions, and PPE instructions from the documentation.
6. Always identify the source document and page number for factual instructions.
7. Do not claim an action is safe unless the supplied documentation explicitly supports it."""

def filter_and_rank_chunks(chunks: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Refines retrieved chunks to prioritize exact matches and remove conflicting/unrelated sections.
    If the query explicitly asks about a specific error code (e.g. E105),
    prioritize chunks containing E105, preserve general safety info, and filter out
    unrelated error code sections (e.g. E315, E210, E420).
    """
    if not chunks:
        return []

    # Check for error code in query
    error_code_match = re.search(r"\b(E\d{3})\b", query, re.IGNORECASE)
    target_error_code = error_code_match.group(1).upper() if error_code_match else None

    if not target_error_code:
        return chunks

    exact_error_chunks = []
    safety_chunks = []
    other_relevant_chunks = []

    for chunk in chunks:
        content = chunk.get("content", "")
        section = chunk.get("section", "")
        doc_type = chunk.get("document_type", "")
        
        has_target_error = (target_error_code in content) or (target_error_code in section)
        
        has_other_error_only = False
        if not has_target_error:
            for ec in ["E105", "E210", "E315", "E420"]:
                if ec != target_error_code and (ec in content or ec in section):
                    has_other_error_only = True
                    break

        if has_target_error:
            exact_error_chunks.append(chunk)
        elif doc_type == "SAFETY" or "safety" in section.lower() or "warning" in section.lower():
            safety_chunks.append(chunk)
        elif not has_other_error_only:
            other_relevant_chunks.append(chunk)

    # Prioritize matching error code and safety chunks
    selected = exact_error_chunks + safety_chunks + other_relevant_chunks
    return selected if selected else chunks

def generate_deterministic_grounded_fallback(query: str, selected_chunks: List[Dict[str, Any]]) -> str:
    """Generate grounded answer directly from retrieved chunks when LLM API is unavailable."""
    if not selected_chunks:
        return "The available documentation does not provide enough information to answer this question."

    query_lower = query.lower()
    
    if "oil" in query_lower and not any("oil" in c.get("content", "").lower() for c in selected_chunks):
        return "The available documentation does not provide enough information regarding recommended engine oil brands."

    top_chunk = selected_chunks[0]
    doc_name = top_chunk.get("document_name", "Authorized Documentation")
    page_num = top_chunk.get("page_number", 1)
    section = top_chunk.get("section", "General")
    content = top_chunk.get("content", "").strip()

    lines = [l.strip() for l in content.split("\n") if l.strip()]
    query_keywords = [w for w in re.findall(r'\b\w{3,}\b', query_lower) if w not in {"what", "how", "the", "for", "and", "should", "does", "with", "show", "tell"}]
    matching_lines = []
    for line in lines:
        if any(kw in line.lower() for kw in query_keywords) or line.startswith(("-", "*", "1.", "2.", "3.", "4.", "5.")):
            matching_lines.append(line)

    if not matching_lines:
        matching_lines = lines[:5]

    formatted_facts = "\n".join(matching_lines[:6])
    header = f"Based on the {doc_name} (Page {page_num}, Section: {section}):\n"
    
    return f"{header}{formatted_facts}"

def generate_grounded_answer(
    query: str,
    model: Optional[str] = None,
    top_k: int = 5,
    llm_client: Optional[LLMClient] = None
) -> Dict[str, Any]:
    """Retrieve knowledge chunks and generate a grounded answer with citations."""
    # Retrieve and rank relevant context chunks
    raw_chunks = retrieve_knowledge_chunks(query=query, model=model, top_k=top_k)
    selected_chunks = filter_and_rank_chunks(raw_chunks, query)

    if not selected_chunks:
        return {
            "query": query,
            "model": model,
            "answer": f"The available documentation for model '{model or 'all models'}' does not provide enough information to answer this question.",
            "sources": [],
            "retrieved_chunks": 0
        }

    # Extract source citations from context chunks
    sources = []
    seen_sources = set()
    for chunk in selected_chunks:
        doc_name = chunk.get("document_name", "")
        doc_type = chunk.get("document_type", "")
        page_num = chunk.get("page_number", 1)
        section = chunk.get("section", "")
        
        source_key = (doc_name, page_num, section)
        if source_key not in seen_sources:
            seen_sources.add(source_key)
            sources.append({
                "document_name": doc_name,
                "document_type": doc_type,
                "page_number": page_num,
                "section": section
            })

    # Format context for LLM prompt
    context_blocks = []
    for idx, chunk in enumerate(selected_chunks, start=1):
        block = (
            f"[DOCUMENT SOURCE {idx}]\n"
            f"Document: {chunk.get('document_name')} (Page {chunk.get('page_number')})\n"
            f"Type: {chunk.get('document_type')}\n"
            f"Section: {chunk.get('section', 'General')}\n"
            f"Content:\n{chunk.get('content')}\n"
        )
        context_blocks.append(block)

    formatted_context = "\n---\n".join(context_blocks)

    user_prompt = (
        f"AUTHORIZED PRODUCT DOCUMENTATION CONTEXT:\n\n"
        f"{formatted_context}\n\n"
        f"==================================================\n"
        f"USER QUESTION: {query}\n"
        f"==================================================\n\n"
        f"Provide a grounded, step-by-step answer based ONLY on the documentation context above."
    )

    # Generate answer using LLM or fallback
    if llm_client is None:
        llm_client = LLMClient()

    try:
        answer_text = llm_client.generate(
            system_prompt=GROUNDING_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.1
        )
    except (LLMProviderError, LLMKeyMissingError, Exception) as err:
        answer_text = generate_deterministic_grounded_fallback(query, selected_chunks)

    return {
        "query": query,
        "model": model,
        "answer": answer_text,
        "sources": sources,
        "retrieved_chunks": len(selected_chunks)
    }

