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
import time
from dotenv import load_dotenv
load_dotenv()


# to make diagram
def save_graph_diagram(graph):
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open("graph_output.png", "wb") as f:
        f.write(png_bytes)

async def run():

    print()
    graph = build_graph()
    save_graph_diagram(graph)

    # scenarios = ["fox", "harrison", "russellmitchell", "santos", "shaw", "wardbeck", "wheeler", "wilson"]
    # for n in scenarios:
    #     data = get_session(n)

    # --- previous single-session run, kept for reference ---
    data = get_session("harrison")
    
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
    
    start_time = time.time()
    result = await graph.ainvoke(initial_state, config=config)
    end_time = time.time()
    ttr_seconds = end_time - start_time
    print(f"Time-to-Recommendation: {ttr_seconds:.2f} seconds")
    
    if "__interrupt__" in result:
        approval = input("Approve this action? (y/n): ")
    
        exec_start = time.time()
        result = await graph.ainvoke(Command(resume=approval), config=config)
        exec_end = time.time()
        exec_seconds = exec_end - exec_start
    
        total_processing_seconds = ttr_seconds + exec_seconds
        print(f"Execution time: {exec_seconds:.2f} seconds")
        print(f"Total Processing Time: {total_processing_seconds:.2f} seconds")
    
        print("Responder Output:", result.get("responder_output"))

#     scenario = "wilson"

#     for data in get_all_sessions(scenario):

#         print(f"=== Running session: {data['session_id']} ===")

#         initial_state = {
#         "session_id": data["session_id"],
#         "alerts": data["alerts"],
#         "alert_log_sequence":data["alert_log_sequence"],
#         "triage_output": None,
#         "investigator_output":None,
#         "adversarial_output":None,
#         "responder_output": None,
#         "revision_count": 0,
#         "human_decision":None,
#         "execution_result": None,

#     }
#         config = {"configurable": {"thread_id": data["session_id"]}}

#         start_time = time.time()
#         result = await graph.ainvoke(initial_state, config=config)
#         end_time = time.time()
#         ttr_seconds = end_time - start_time
#         print(f"Time-to-Recommendation: {ttr_seconds:.2f} seconds")

#         if "__interrupt__" in result:
#             approval = input("Approve this action? (y/n): ")

#             exec_start = time.time()
#             result = await graph.ainvoke(Command(resume=approval), config=config)
#             exec_end = time.time()
#             exec_seconds = exec_end - exec_start

#             total_processing_seconds = ttr_seconds + exec_seconds
#             print(f"Execution time: {exec_seconds:.2f} seconds")
#             print(f"Total Processing Time: {total_processing_seconds:.2f} seconds")

#             print("Responder Output:", result.get("responder_output"))

if __name__ == "__main__":
    asyncio.run(run())