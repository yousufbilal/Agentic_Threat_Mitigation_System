import json
from langchain_ollama import ChatOllama  # Swapped from langchain_openai
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from langgraph.graph import END, START, StateGraph


def triage_agent_node(state: GraphState) -> GraphState:

    return(GraphState(nlist=["Yousuf"]))






