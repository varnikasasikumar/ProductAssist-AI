import re
import json
from typing import Dict, Any, List, Optional

from rag.retriever import retrieve_knowledge_chunks
from rag.answer_generator import filter_and_rank_chunks
from rag.llm import LLMClient, LLMKeyMissingError, LLMProviderError
from .session_store import session_store, TroubleshootingSession
from .safety_layer import apply_safety_checks

ORCHESTRATOR_SYSTEM_PROMPT = """You are ProductAssist AI's Troubleshooting Agent for industrial equipment.

Your task is to analyze the user's problem, review current diagnostic session history and documentation context, and determine the NEXT action:
1. ASK_QUESTION: Ask a targeted diagnostic question to isolate the cause. (status: DIAGNOSING)
2. PROVIDE_CORRECTIVE_ACTION: Provide grounded step-by-step corrective procedures and safety warnings for an identified root cause, asking the user to execute the procedure and verify system operation. (status: CORRECTIVE_ACTION or VERIFYING)
3. RESOLVE: Confirm that the user's latest response verifies successful resolution / normal operation. (status: RESOLVED)
4. ESCALATE: State that available documentation is insufficient or technical field service escalation is required. (status: ESCALATED)

CRITICAL RULES:
1. Base your diagnostic steps ONLY on the provided authorized product documentation.
2. Do NOT invent procedures, error codes, component names, or unverified fixes.
3. If an error code is present (e.g. E105), identify the issue name (e.g., 'Error Code E105 - Cooling System Malfunction') and ask about documented causes one step at a time.
4. When a cause is identified from user feedback, select PROVIDE_CORRECTIVE_ACTION. Do NOT mark as RESOLVED immediately; provide instructions and ask the user to verify system flow/operation.
5. Only select RESOLVE when the user explicitly confirms that the corrective action was completed and the machine is operating normally or the issue is resolved.
6. For safety-sensitive actions (servicing electrical cabinet, opening pump enclosure), include explicit safety warnings.
7. If documentation does not cover the problem or diagnostic options are exhausted without resolution, select ESCALATE.

You MUST return ONLY a JSON object with this EXACT structure:
{
  "action": "ASK_QUESTION" | "PROVIDE_CORRECTIVE_ACTION" | "RESOLVE" | "ESCALATE",
  "identified_issue": "Issue Name (e.g. Error Code E105 - Cooling System Malfunction)",
  "message": "User-facing diagnostic assessment, corrective instructions, or resolution summary",
  "next_question": "Targeted diagnostic question or verification question (e.g. 'Please refill coolant to 80% capacity and clean intake screen. Once completed, restart system. Is coolant flow rate FM-1 back above 8.0 L/min?'), or empty string if RESOLVED/ESCALATED",
  "reasoning_summary": "Short user-safe reasoning summary",
  "status": "DIAGNOSING" | "CORRECTIVE_ACTION" | "VERIFYING" | "RESOLVED" | "ESCALATED"
}"""

def parse_llm_json(raw_text: str) -> Dict[str, Any]:
    """Parse JSON payload from LLM output cleanly."""
    clean_text = raw_text.strip()
    if "```json" in clean_text:
        clean_text = clean_text.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_text:
        clean_text = clean_text.split("```")[1].split("```")[0].strip()
    
    try:
        return json.loads(clean_text)
    except Exception:
        # Fallback if LLM generated prose instead of JSON
        return {
            "action": "ASK_QUESTION",
            "identified_issue": None,
            "message": raw_text,
            "next_question": "Could you provide any additional diagnostic details or error codes shown on the display?",
            "reasoning_summary": "Processed general text response.",
            "status": "DIAGNOSING"
        }

def start_troubleshooting(model: str, problem: str, llm_client: Optional[LLMClient] = None) -> Dict[str, Any]:
    """
    Starts a new agentic troubleshooting session.
    1. Creates session state.
    2. Uses RAG retrieval to find relevant documentation.
    3. Prompts LLM to analyze issue, identify error code, and choose first diagnostic step.
    4. Applies safety layer and updates state.
    """
    session = session_store.create_session(model=model, problem=problem)
    return _run_orchestrator_turn(session=session, latest_user_response=None, llm_client=llm_client)

def continue_troubleshooting(session_id: str, user_response: str, llm_client: Optional[LLMClient] = None) -> Dict[str, Any]:
    """
    Continues an existing troubleshooting session with user's diagnostic observation.
    """
    session = session_store.get_session(session_id)
    if not session:
        raise ValueError(f"Session ID '{session_id}' not found.")

    if session.status in ["RESOLVED", "ESCALATED"]:
        # Session completed, return current state
        return {
            "session_id": session.session_id,
            "model": session.model,
            "identified_issue": session.identified_issue,
            "message": f"This troubleshooting session is already {session.status.lower()}.",
            "next_question": "",
            "status": session.status,
            "reasoning_summary": f"Session marked as {session.status}.",
            "sources": session.sources
        }

    # Add user's latest response to diagnostic history
    last_q = session.diagnostic_answers[-1]["question"] if session.diagnostic_answers else "Initial Problem"
    session.add_diagnostic_answer(question=last_q, answer=user_response)

    return _run_orchestrator_turn(session=session, latest_user_response=user_response, llm_client=llm_client)

def _run_orchestrator_turn(
    session: TroubleshootingSession,
    latest_user_response: Optional[str] = None,
    llm_client: Optional[LLMClient] = None
) -> Dict[str, Any]:
    
    # Retrieve RAG context for problem and diagnostic history
    search_query = f"{session.problem} {' '.join(a['answer'] for a in session.diagnostic_answers)}"
    raw_chunks = retrieve_knowledge_chunks(query=search_query, model=session.model, top_k=5)
    selected_chunks = filter_and_rank_chunks(raw_chunks, search_query)

    # Check documentation coverage
    is_unknown_issue = False
    if not selected_chunks or (len(session.problem) > 10 and not any(ec in session.problem for ec in ["E105", "E210", "E315", "E420", "filter", "coolant", "spindle", "power", "network", "ppe"]) and all(c.get("score", 2.0) > 1.4 for c in selected_chunks)):
        is_unknown_issue = True

    if is_unknown_issue and session.current_step == 1:
        session.status = "ESCALATED"
        session_store.save_session(session)
        return {
            "session_id": session.session_id,
            "model": session.model,
            "identified_issue": None,
            "message": f"The available documentation for model '{session.model}' does not provide sufficient diagnostic information for this specific problem statement.",
            "next_question": "We recommend escalating this issue to a qualified field service technician.",
            "status": "ESCALATED",
            "reasoning_summary": "Insufficient documentation coverage for unknown symptom.",
            "sources": []
        }

    # Extract source citations
    sources = []
    seen_sources = set()
    for chunk in selected_chunks:
        doc_name = chunk.get("document_name", "")
        doc_type = chunk.get("document_type", "")
        page_num = chunk.get("page_number", 1)
        sec = chunk.get("section", "")
        s_key = (doc_name, page_num, sec)
        if s_key not in seen_sources:
            seen_sources.add(s_key)
            sources.append({
                "document_name": doc_name,
                "document_type": doc_type,
                "page_number": page_num,
                "section": sec
            })

    # Format context and history for LLM
    context_blocks = []
    for idx, c in enumerate(selected_chunks, start=1):
        context_blocks.append(
            f"[DOC {idx}] {c.get('document_name')} (Page {c.get('page_number')}) - Section: {c.get('section')}\n{c.get('content')}"
        )
    formatted_context = "\n\n".join(context_blocks)

    history_blocks = [f"Initial Problem: {session.problem}"]
    for idx, ans in enumerate(session.diagnostic_answers, start=1):
        history_blocks.append(f"Q{idx}: {ans['question']}\nA{idx}: {ans['answer']}")
    formatted_history = "\n".join(history_blocks)

    user_prompt = (
        f"MODEL: {session.model}\n\n"
        f"DIAGNOSTIC HISTORY:\n{formatted_history}\n\n"
        f"AUTHORIZED DOCUMENTATION CONTEXT:\n{formatted_context}\n\n"
        f"Determine the next diagnostic step and return ONLY JSON."
    )

    # Invoke LLM diagnostic orchestrator
    if llm_client is None:
        llm_client = LLMClient()

    try:
        raw_llm_output = llm_client.generate(
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.1
        )
        decision = parse_llm_json(raw_llm_output)
    except (LLMProviderError, LLMKeyMissingError) as err:
        # Fallback decision engine when live API key is unavailable
        prob_lower = session.problem.lower()
        hist_str = " ".join(a["answer"].lower() for a in session.diagnostic_answers)
        
        if "e105" in prob_lower or "coolant" in prob_lower:
            if not session.diagnostic_answers:
                decision = {
                    "action": "ASK_QUESTION",
                    "identified_issue": "Error Code E105 - Cooling System Malfunction",
                    "message": "Error Code E105 indicates a Cooling System Malfunction (coolant flow below 8.0 L/min or pump overload Q4). Let's troubleshoot step-by-step.",
                    "next_question": "Before continuing, please check the coolant reservoir sight glass. Is the coolant level below the MIN marking?",
                    "reasoning_summary": "Fallback decision engine: Identified E105. Asking coolant level diagnostic question.",
                    "status": "DIAGNOSING"
                }
            elif "below min" in hist_str or "low" in hist_str:
                if session.status != "CORRECTIVE_ACTION":
                    decision = {
                        "action": "PROVIDE_CORRECTIVE_ACTION",
                        "identified_issue": "Error Code E105 - Cooling System Malfunction",
                        "message": (
                            "Root cause identified: Low coolant level.\n\n"
                            "SAFETY PRECAUTION: Always turn OFF main electrical breaker before servicing components.\n\n"
                            "RECOMMENDED CORRECTIVE ACTIONS:\n"
                            "1. Turn OFF main electrical power disconnect switch on rear cabinet.\n"
                            "2. Top up coolant tank with 6% water-soluble synthetic coolant emulsion to 80% capacity.\n"
                            "3. Inspect intake screen for sludge/chips and flush if needed."
                        ),
                        "next_question": "Please perform these corrective steps and restart the pump. Is the coolant flow restored and E105 cleared?",
                        "reasoning_summary": "Fallback decision engine: Provided corrective actions for low coolant level.",
                        "status": "CORRECTIVE_ACTION"
                    }
                else:
                    decision = {
                        "action": "RESOLVE",
                        "identified_issue": "Error Code E105 - Cooling System Malfunction",
                        "message": "Troubleshooting completed successfully. The cooling system is now operating normally and Error Code E105 is resolved.",
                        "next_question": "",
                        "reasoning_summary": "Fallback decision engine: Verified user resolution.",
                        "status": "RESOLVED"
                    }
            else:
                decision = {
                    "action": "ASK_QUESTION",
                    "identified_issue": "Error Code E105 - Cooling System Malfunction",
                    "message": "Analyzing cooling system diagnostics...",
                    "next_question": "Is thermal overload relay Q4 tripped inside the electrical cabinet?",
                    "reasoning_summary": "Fallback decision engine: Asking follow-up question.",
                    "status": "DIAGNOSING"
                }
        else:
            decision = {
                "action": "ASK_QUESTION",
                "identified_issue": "General Diagnostic",
                "message": f"Diagnostic session active for model {session.model}.",
                "next_question": "Could you provide any additional diagnostic details or display error codes?",
                "reasoning_summary": "Fallback decision engine: General diagnostic step.",
                "status": "DIAGNOSING"
            }

    # Apply safety checks
    safety_checked = apply_safety_checks(
        message=decision.get("message", ""),
        next_question=decision.get("next_question", ""),
        retrieved_chunks=selected_chunks
    )

    # Update session state
    session.identified_issue = decision.get("identified_issue") or session.identified_issue
    session.sources = sources

    action = decision.get("action", "ASK_QUESTION")
    dec_status = decision.get("status")

    if action in ["RESOLVE", "PROVIDE_GUIDANCE"] and dec_status == "RESOLVED":
        session.status = "RESOLVED"
        session.resolution = safety_checked["message"]
    elif action == "PROVIDE_CORRECTIVE_ACTION" or dec_status in ["CORRECTIVE_ACTION", "VERIFYING"]:
        session.status = dec_status if dec_status in ["CORRECTIVE_ACTION", "VERIFYING"] else "CORRECTIVE_ACTION"
    elif action == "ESCALATE" or dec_status == "ESCALATED":
        session.status = "ESCALATED"
    else:
        session.status = "DIAGNOSING"

    session_store.save_session(session)

    return {
        "session_id": session.session_id,
        "model": session.model,
        "identified_issue": session.identified_issue,
        "message": safety_checked["message"],
        "next_question": safety_checked["next_question"],
        "status": session.status,
        "reasoning_summary": decision.get("reasoning_summary", "Diagnostic step evaluated."),
        "sources": sources
    }
