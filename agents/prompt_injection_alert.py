from graph.state import GraphState
import json
import os

MODEL_NAME = "gemini-3.7-flash"

os.makedirs(f"prompt_injection_alert", exist_ok=True)

def prompt_injection_alert(state:GraphState) -> GraphState:

    triage_output = state["triage_output"]
    adversarial_output = state["adversarial_output"]

    print()
    print("*** Prompt Injection Alert Sent ***") 
    print()

    with open(f"prompt_injection_alert/prompt_injection_alert_result.json", "w") as file:
        json.dump({"triage_output": triage_output, "adversarial_output": adversarial_output}, file, indent=2)