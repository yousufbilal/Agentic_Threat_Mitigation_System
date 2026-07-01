from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

# 1. Define the simplest possible State (a dictionary)
class State(dict):
    fruit: str

# 2. Your worker function
def devil_fruit(state):
    llm = ChatOllama(model="qwen2.5:3b")
    response = llm.invoke(state["fruit"])
    return {"fruit": response.content}


# 3. Build the path
builder = StateGraph(dict)
builder.add_node("node", devil_fruit)
builder.add_edge(START, "node")
builder.add_edge("node", END)

# 4. Run it
graph = builder.compile()
result = graph.invoke({"fruit": "what is a devil fruit in one piece?"})
print(result["fruit"])