from graph.state import GraphState
from langgraph.graph import StateGraph, START, END
from agents.triage_agent import triage_agent
from agents.investigator_agent import investigator_agent


def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("triage", triage_agent)
    builder.add_node("investigator", investigator_agent)


    # Edges
    builder.add_edge(START, "triage")
    builder.add_edge("triage", "investigator")
    builder.add_edge("investigator", END)

    # Compile
    graph = builder.compile()

    return graph
