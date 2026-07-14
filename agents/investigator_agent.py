from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  

llm = ChatOllama(model="qwen2.5:3b")

def investigator_agent(state:GraphState)-> GraphState:

    alerts = state["alerts"]
    triage_output = state["triage_output"]

    system_prompt = SystemMessage(content="""You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.
    Your only task:
    identify the likely attack technique or pattern in this alert sequence, and which account or host it affects.
    Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.
    Output format: {"attack_technique": "short label", "affected_entity": "account/host from the data",
    "summary": "one sentence explanation that names the actual events_id or rule_id values from the alert data above"}""")

    human_prompt = HumanMessage(content=str({"alerts": alerts, "triage_output": triage_output}))

    response = llm.invoke([system_prompt, human_prompt])

    print(response.content)

    return GraphState(
        investigator_output={"raw_response": response.content}
    )