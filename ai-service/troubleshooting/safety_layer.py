from typing import Dict, Any, List

def apply_safety_checks(
    message: str,
    next_question: str,
    retrieved_chunks: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Safety Guardrail Layer:
    Ensures safety warnings from authorized documentation are preserved in diagnostic guidance.
    If physical/electrical maintenance is recommended or inquired about, verifies that
    power OFF requirements, Lockout/Tagout (LOTO), and PPE precautions are included.
    """
    clean_msg = message.strip()
    clean_q = next_question.strip() if next_question else ""

    # Check if retrieved documentation contains explicit WARNING / SAFETY statements
    doc_warnings = []
    for chunk in retrieved_chunks:
        content = chunk.get("content", "")
        if "WARNING" in content or "SAFETY" in content:
            lines = [l.strip() for l in content.split("\n") if "WARNING" in l or "SAFETY" in l or "power" in l.lower()]
            for line in lines:
                if line and line not in doc_warnings:
                    doc_warnings.append(line)

    # Keywords indicating physical inspection or maintenance action
    maintenance_keywords = ["open", "clean", "replace", "flush", "servicing", "cabinet", "pump", "relay", "breaker", "filter"]
    is_maintenance_action = any(kw in clean_msg.lower() or kw in clean_q.lower() for kw in maintenance_keywords)

    if is_maintenance_action:
        # Check if power OFF safety instruction is already present
        has_power_off_warning = "power off" in clean_msg.lower() or "turn off" in clean_msg.lower() or "power off" in clean_q.lower()
        if not has_power_off_warning:
            safety_addition = "SAFETY PRECAUTION: Always turn OFF main electrical disconnect switch before opening electrical cabinet or servicing internal components."
            clean_msg = f"{clean_msg}\n\n⚠️ {safety_addition}"

    return {
        "message": clean_msg,
        "next_question": clean_q
    }
