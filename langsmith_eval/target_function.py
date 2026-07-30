from graph.workflow import build_graph
from langgraph.types import Command
import asyncio
from tools.session_loader import get_session

async def target(inputs: dict) -> dict:
    graph = build_graph()

    alerts = inputs["alerts"]
    alert_log_sequence = [alert["full_log"] for alert in alerts]

    initial_state = {
        "session_id": "eval",
        "alerts": alerts,
        "alert_log_sequence": alert_log_sequence,
        "triage_output": None,
        "investigator_output": None,
        "adversarial_output": None,
        "responder_output": None,
        "revision_count": 0,
        "human_decision": None,
        "execution_result": None,
    }

    config = {"configurable": {"thread_id": "eval-run"}}

    result = await graph.ainvoke(initial_state, config=config)

    if "__interrupt__" in result:
        result = await graph.ainvoke(Command(resume="y"), config=config)

    return result["responder_output"]
    # return result["triage_output"]

if __name__ == "__main__":
    data = get_session("fox")
    test_input = {"alerts": data["alerts"]}

    result = asyncio.run(target(test_input))
    print()
    print("THE IS THE TARGET FUNCTION---->",result)
    print()