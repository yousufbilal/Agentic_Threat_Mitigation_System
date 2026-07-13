from langchain_ollama import ChatOllama  # Swapped from langchain_openai
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  

def triage_agent(state: GraphState) -> GraphState:
    
    return(GraphState(nlist=["Yousuf"]))