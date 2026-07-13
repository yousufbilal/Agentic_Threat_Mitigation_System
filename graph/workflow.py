from graph.state import GraphState
from langgraph.graph import StateGraph, START, END
from agents.triage_agent import triage_agent


def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("triage", triage_agent)

    # Edges
    builder.add_edge(START, "triage")
    builder.add_edge("triage", END)

    # Compile
    graph = builder.compile()

    return graph
