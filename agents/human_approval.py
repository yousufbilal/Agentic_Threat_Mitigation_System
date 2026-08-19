from graph.state import GraphState
from langgraph.types import interrupt
import json
import os

MODEL_NAME = "gemini-3.7-flash"


def human_approval(state: GraphState) -> GraphState:

    responder_output = state["responder_output"]
    session_id = state["session_id"]

    decision = interrupt({"responder_output": responder_output})

    if decision == "y":
        os.makedirs(f"responder_output/{MODEL_NAME}", exist_ok=True)
        with open(f"responder_output/{MODEL_NAME}/{session_id}_result.json", "w") as file:
            json.dump(responder_output, file, indent=2)

    print(f"Human decision: {decision}")

    return GraphState(human_decision=decision)