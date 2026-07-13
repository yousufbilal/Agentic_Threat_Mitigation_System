from graph.state import GraphState
from langgraph.graph import StateGraph, START, END
from agents import triage_agent



def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("triage", triage_agent)

    # Edges
    builder.add_edge(START, "triage_agent")
    builder.add_edge(triage_agent, "END")

    # Compile
    return builder.compile()