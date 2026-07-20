import warnings
warnings.filterwarnings("ignore", message=".*allowed_objects.*")

from graph.workflow import build_graph
from graph.state import GraphState
from tools.preprocess_ait_data import get_fox_session
from tools.session_loader import get_session

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
    "responder_output": None
}
    result = graph.invoke(initial_state)
    # print(result)


if __name__ == "__main__":
    run()