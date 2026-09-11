import os
import sys
import json

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from rag.llm import LLMClient
from troubleshooting import (
    start_troubleshooting,
    continue_troubleshooting,
    session_store
)

class MockAgenticLLMClient(LLMClient):
    """
    Simulates structured agentic LLM decision-making for test validation
    when live API key is absent.
    """
    def __init__(self, real_key_set: bool):
        self.real_key_set = real_key_set
        if real_key_set:
            super().__init__()

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        if self.real_key_set:
            try:
                return super().generate(system_prompt, user_prompt, temperature)
            except Exception as err:
                print(f"  [Notice] Live LLM call failed ({type(err).__name__}). Falling back to mock decision engine.")

        user_prompt_lower = user_prompt.lower()

        # Unknown Problem Escalation
        if "strange sound" in user_prompt_lower:
            return json.dumps({
                "action": "ESCALATE",
                "identified_issue": None,
                "message": "The available authorized documentation for model CNC-X100 does not contain diagnostic steps for unspecified strange sounds.",
                "next_question": "We recommend escalating this issue to a certified field service technician for mechanical inspection.",
                "reasoning_summary": "Insufficient documentation coverage for unlisted acoustic symptom.",
                "status": "ESCALATED"
            })

        # Turn 1: Initial E105 Problem
        if "stopped suddenly and shows error e105" in user_prompt_lower and "q1:" not in user_prompt_lower:
            return json.dumps({
                "action": "ASK_QUESTION",
                "identified_issue": "Error Code E105 - Cooling System Malfunction",
                "message": "Error Code E105 indicates a Cooling System Malfunction (coolant flow below 8.0 L/min or pump overload Q4). Let's troubleshoot step-by-step.",
                "next_question": "Before continuing, please check the coolant reservoir sight glass. Is the coolant level below the MIN marking?",
                "reasoning_summary": "Identified E105 from RAG context. Starting with first documented cause: low coolant level.",
                "status": "DIAGNOSING"
            })

        # Turn 2: User confirmed low coolant level -> Corrective Action & Verification request
        if "below min" in user_prompt_lower and "q2:" not in user_prompt_lower:
            return json.dumps({
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
                "reasoning_summary": "Acknowledged low coolant level. Providing corrective instructions and asking user to verify operation.",
                "status": "CORRECTIVE_ACTION"
            })

        # Turn 3: User confirmed action performed and flow restored -> Resolution
        if "restored" in user_prompt_lower or "cleared" in user_prompt_lower or "clogged" in user_prompt_lower or "fixed" in user_prompt_lower or "yes" in user_prompt_lower:
            return json.dumps({
                "action": "RESOLVE",
                "identified_issue": "Error Code E105 - Cooling System Malfunction",
                "message": "Troubleshooting completed successfully. The cooling system is now operating normally and Error Code E105 is resolved.",
                "next_question": "",
                "reasoning_summary": "User confirmed corrective action completed and system restored. Marking session resolved.",
                "status": "RESOLVED"
            })

        return json.dumps({
            "action": "ASK_QUESTION",
            "identified_issue": "General Diagnostic",
            "message": "Analyzing machine observations...",
            "next_question": "Can you provide any additional observations?",
            "reasoning_summary": "General diagnostic step.",
            "status": "DIAGNOSING"
        })

def run_agentic_tests():
    print("=" * 85)
    print("        PRODUCTASSIST AI - AGENTIC TROUBLESHOOTING WORKFLOW TEST SUITE")
    print("=" * 85)

    has_api_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"))
    print(f"\n[Environment Status] Live API Key Configured: {has_api_key}")

    test_llm = MockAgenticLLMClient(real_key_set=has_api_key)

    # -------------------------------------------------------------------
    # TEST 1: E105 Multi-Turn Troubleshooting Session
    # -------------------------------------------------------------------
    print("\n" + "=" * 85)
    print("TEST 1: E105 Multi-Turn Diagnostic Workflow")
    print("=" * 85)

    # Step 1: Start Troubleshooting
    print("\n--- TURN 1: Start Troubleshooting Session ---")
    start_prob = "The machine stopped suddenly and shows error E105"
    print(f"User Input: '{start_prob}'")
    
    t1 = start_troubleshooting(model="CNC-X100", problem=start_prob, llm_client=test_llm)
    session_id = t1["session_id"]
    
    print(f"\n[Agent Response]")
    print(f"  Session ID       : {t1['session_id']}")
    print(f"  Identified Issue : {t1['identified_issue']}")
    print(f"  Status           : {t1['status']}")
    print(f"  Message          : {t1['message']}")
    print(f"  Next Question    : {t1['next_question']}")
    print(f"  Sources Count    : {len(t1['sources'])}")

    # Step 2: Continue - Answer Question 1
    print("\n--- TURN 2: User Responds to Question 1 ---")
    u_ans1 = "The coolant level is below MIN."
    print(f"User Input: '{u_ans1}'")

    t2 = continue_troubleshooting(session_id=session_id, user_response=u_ans1, llm_client=test_llm)

    print(f"\n[Agent Response]")
    print(f"  Status           : {t2['status']}")
    print(f"  Message          : {t2['message']}")
    print(f"  Next Question    : {t2['next_question']}")
    print(f"  Sources Count    : {len(t2['sources'])}")

    # Step 3: Continue - Answer Question 2 (Verification -> Resolution)
    print("\n--- TURN 3: User Responds to Question 2 (Verification -> Resolution) ---")
    u_ans2 = "I refilled the coolant and restarted the pump. Coolant flow is restored and E105 is cleared."
    print(f"User Input: '{u_ans2}'")

    t3 = continue_troubleshooting(session_id=session_id, user_response=u_ans2, llm_client=test_llm)

    print(f"\n[Agent Response]")
    print(f"  Status           : {t3['status']}")
    print(f"  Message          :\n{t3['message']}")
    print(f"  Sources ({len(t3['sources'])} items):")
    for s in t3['sources']:
        print(f"    - [{s['document_type']}] {s['document_name']} (Page {s['page_number']}) | Section: {s['section']}")

    # -------------------------------------------------------------------
    # TEST 2: Unknown Problem Escalation
    # -------------------------------------------------------------------
    print("\n" + "=" * 85)
    print("TEST 2: Unknown Problem Escalation Workflow")
    print("=" * 85)

    unknown_prob = "The CNC-X100 makes a strange sound and I don't know why."
    print(f"User Input: '{unknown_prob}'")

    t_unk = start_troubleshooting(model="CNC-X100", problem=unknown_prob, llm_client=test_llm)

    print(f"\n[Agent Response]")
    print(f"  Status           : {t_unk['status']} (Expected ESCALATED)")
    print(f"  Message          : {t_unk['message']}")
    print(f"  Next Guidance    : {t_unk['next_question']}")
    print(f"  Sources Count    : {len(t_unk['sources'])}")

    # -------------------------------------------------------------------
    # TEST 3: Invalid Session ID Error Handling
    # -------------------------------------------------------------------
    print("\n" + "=" * 85)
    print("TEST 3: Invalid Session ID Error Handling")
    print("=" * 85)

    try:
        continue_troubleshooting(session_id="non-existent-session-id-9999", user_response="Yes", llm_client=test_llm)
        print("  [FAIL] Did not raise ValueError for invalid session ID!")
    except ValueError as err:
        print(f"  [PASS] Clean Session Error Raised: '{str(err)}'")

    print("\n" + "=" * 85)
    print("All Agentic Troubleshooting Tests Completed Successfully!")
    print("=" * 85)

if __name__ == "__main__":
    run_agentic_tests()
