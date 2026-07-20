import warnings
# to ignore dependency warnining which was annoying 
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)

from graph.workflow import build_graph
from graph.state import GraphState
from tools.preprocess_ait_data import get_fox_session
from tools.session_loader import get_session
from langgraph.types import Command


def save_graph_diagram(graph):
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open("graph_output.png", "wb") as f:
        f.write(png_bytes)

def run():
    print()
    graph = build_graph()
    save_graph_diagram(graph)

    # data = get_fox_session()
    data = get_session("fox")

    initial_state = {
    "session_id": data["session_id"],
    "alerts": data["alerts"],
    "triage_output": None,
    "investigator_output":None,
    "adversarial_output":None,
    "responder_output": None,
    "revision_count": 0,
    "human_decision":None,
    "execution_result": None,

}
    config = {"configurable": {"thread_id": data["session_id"]}}

    result = graph.invoke(initial_state, config=config)

    if "__interrupt__" in result:
        print("\n--- HUMAN APPROVAL REQUIRED ---")
        print(result["__interrupt__"][0].value)
        approval = input("\nApprove this action? (y/n): ")
        result = graph.invoke(Command(resume=approval), config=config)
        print(result)

if __name__ == "__main__":
    run()