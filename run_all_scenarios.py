import warnings
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainPendingDeprecationWarning)
from graph.workflow import build_graph
from tools.session_loader import get_session
from langgraph.types import Command
import asyncio
import time
from dotenv import load_dotenv
load_dotenv()


SCENARIOS = ["fox", "harrison", "russellmitchell", "santos", "shaw", "wardbeck", "wheeler", "wilson"]

async def run_one(graph, scenario):
    data = get_session(scenario)

    initial_state = {
        "session_id": data["session_id"],
        "alerts": data["alerts"],
        "alert_log_sequence": data["alert_log_sequence"],
        "triage_output": None,
        "investigator_output": None,
        "adversarial_output": None,
        "responder_output": None,
        "revision_count": 0,
        "human_decision": None,
        "execution_result": None,
    }
    config = {"configurable": {"thread_id": data["session_id"]}}

    start_time = time.time()
    result = await graph.ainvoke(initial_state, config=config)
    end_time = time.time()
    ttr_seconds = end_time - start_time
    print(f"Time-to-Recommendation: {ttr_seconds:.2f} seconds")

    if "__interrupt__" in result:
        approval = "y"
        print(f"Approve this action? (y/n): {approval}")

        exec_start = time.time()
        result = await graph.ainvoke(Command(resume=approval), config=config)
        exec_end = time.time()
        exec_seconds = exec_end - exec_start

        total_processing_seconds = ttr_seconds + exec_seconds
        print(f"Execution time: {exec_seconds:.2f} seconds")
        print(f"Total Processing Time: {total_processing_seconds:.2f} seconds")

        print("Responder Output:", result.get("responder_output"))
    else:
        print("No interrupt reached. Final result:", result)

async def main():
    graph = build_graph()

    for scenario in SCENARIOS:
        print(f"\n{'='*70}\nRUNNING SCENARIO: {scenario}\n{'='*70}\n")
        await run_one(graph, scenario)

if __name__ == "__main__":
    asyncio.run(main())

