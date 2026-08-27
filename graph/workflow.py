from graph.state import GraphState
from langgraph.graph import StateGraph, START, END
from agents.triage_agent import triage_agent
from agents.investigator_agent import investigator_agent
from agents.adversarial_agent import adversarial_agent
from agents.responder_agent import responder_agent
from typing import Literal
from langgraph.checkpoint.memory import InMemorySaver
from agents.human_approval import human_approval
from agents.prompt_injection_alert import prompt_injection_alert

def route_after_triage(state: GraphState) -> Literal["investigator","prompt_injection_alert", END]:
    if state["triage_output"]["prompt_injection_detected"] == True:
        return "prompt_injection_alert"
    elif state["triage_output"]["mitigation_required"] == True:
        return "investigator"
    else:
        return END
    
    # the revision count here is for how many times i wanna run the loop 
def route_after_adversal(state: GraphState) -> Literal["investigator", "responder","prompt_injection_alert"]:
    if state["adversarial_output"]["prompt_injection_detected"] == True:
        return "prompt_injection_alert"
    elif state["adversarial_output"]["verdict"] == "rejected" and state["revision_count"] <= 2:
        return "investigator"
    else:
        return "responder"



def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("triage", triage_agent)
    builder.add_node("investigator", investigator_agent)
    builder.add_node("adversarial", adversarial_agent)
    builder.add_node("responder", responder_agent)
    builder.add_node("prompt_injection_alert", prompt_injection_alert)
    builder.add_node("human_approval", human_approval)


    # Edges
    builder.add_edge(START, "triage")
    builder.add_conditional_edges("triage", route_after_triage)
    builder.add_edge("investigator", "adversarial")
    builder.add_conditional_edges("adversarial", route_after_adversal)
    builder.add_edge("responder", "human_approval")
    builder.add_edge("human_approval", END)


    # Compile
    graph = builder.compile(checkpointer=InMemorySaver())

    return graph
