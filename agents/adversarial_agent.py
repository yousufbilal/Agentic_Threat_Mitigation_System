from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  

llm = ChatOllama(model="qwen2.5:3b")

def adversarial_agent(state:GraphState) -> GraphState:

    # print("adversarial agent node received this", state["session_id"])
    alerts = state["alerts"]
    investigator_output = state["investigator_output"]
    triage_output= state["triage_output"]

    system_prompt = SystemMessage(content="""You are a SOC adversarial reviewer challenging an investigator's conclusion about a security alert sequence.
    Your only task:
    determine whether the investigator's attack_technique and affected_entity are actually supported by the alert data and triage reasoning provided below, 
    or whether the conclusion overreaches, ignores an alternative explanation (e.g. false positive, benign admin activity), or is not backed by the cited events.
    Base your review only on the alert data, triage reasoning, and investigator output provided below. Do not assume information that isn't present.
    Output format: {"verdict": "confirmed" or "revised" or "rejected", "revised_technique": "short label or null if confirmed", "reasoning": "one sentence explanation that names the actual events_id or rule_id values from the alert data above that support the verdict"}
    """)

    human_prompt = HumanMessage(content=str({"alerts":alerts, "investigator_output":investigator_output, "triage_output":triage_output }))

    response = llm.invoke([system_prompt, human_prompt])
    # print(response.content)
    
    return GraphState(
    adversarial_agent_output={"adversarial_response": response.content}
)
