import warnings
# to ignore dependency warnining which was annoying 
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)
from graph.workflow import build_graph
from graph.state import GraphState
from tools.session_loader import get_session
from langgraph.types import Command
import json
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

print(os.environ.get("LANGSMITH_API_KEY"))

# to make diagram
def save_graph_diagram(graph):
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open("graph_output.png", "wb") as f:
        f.write(png_bytes)

async def run():
    print()
    graph = build_graph()
    save_graph_diagram(graph)

    data = get_session("fox")

    print(len(data["alerts"]))
          
    initial_state = {
    "session_id": data["session_id"],
    "alerts": data["alerts"],
    "alert_log_sequence":data["alert_log_sequence"],
    "triage_output": None,
    "investigator_output":None,
    "adversarial_output":None,
    "responder_output": None,
    "revision_count": 0,
    "human_decision":None,
    "execution_result": None,

}
    config = {"configurable": {"thread_id": data["session_id"]}}
    result = await graph.ainvoke(initial_state, config=config)

    if "__interrupt__" in result:
        approval = input("Approve this action? (y/n): ")
        result = await graph.ainvoke(Command(resume=approval), config=config)

if __name__ == "__main__":
    asyncio.run(run())