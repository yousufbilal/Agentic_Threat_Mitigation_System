from graph.workflow import build_graph
from graph.state import GraphState


def save_graph_diagram(graph):

    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("graph_output.png", "wb") as f:
        f.write(png_bytes)


def run():

    graph = build_graph()

    save_graph_diagram(graph)

    initial_state = GraphState(
        session_id="agent_27",
        alert_ids=[],
        raw_alerts=[],
        triage_output=None
    )

    result = graph.invoke(initial_state)

    print(result)


if __name__ == "__main__":
    run()