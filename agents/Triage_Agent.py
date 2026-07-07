import chromadb
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


client = chromadb.PersistentClient(path="../chroma_data")

collection = client.get_collection(name="wazuh_alerts")

print(f"Database connected. Total records: {collection.get()}")

# class GraphState(TypedDict):
#     input_text: str
#     processed_data: list[str]

# def node_one(state: GraphState) -> dict:
#     print("--- Executing Node 1 ---")
#     return {"processed_text": state["input_text"].upper()}

# def node_two(state: GraphState) -> dict:
#     print("--- Executing Node 2 ---")
#     return {"processed_text": state["processed_text"] + "!!!"}


# def process(self):
#         # Process the input text and generate processed data
#         self.processed_data = self.input_text.split()  # Example processing


# # 3. Build the Graph
# builder = StateGraph(GraphState)

# # Add nodes
# builder.add_node("transform_upper", node_one)
# builder.add_node("add_exclamation", node_two)

# # Define flow (edges)
# builder.add_edge(START, "transform_upper")
# builder.add_edge("transform_upper", "add_exclamation")
# builder.add_edge("add_exclamation", END)

# # Compile the graph into an executable runnable
# graph = builder.compile()

# # 4. Invoke the Graph
# initial_state = {"input_text": "hello langgraph"}
# result = graph.invoke(initial_state)

# print("\nFinal Result:", result)
