from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState
from pydantic import BaseModel
from typing import Literal

class TriageOutput(BaseModel):
    mitigation_required: bool
    reasoning: str
    severity: Literal["Low", "Medium", "High"]

llm = ChatOllama(model="qwen2.5:3b", temperature=0)
structured_llm = llm.with_structured_output(TriageOutput)


def triage_agent(state: GraphState) -> GraphState:

    alerts = state['alerts']

    system_prompt = SystemMessage(content="""You are a SOC triage analyst reviewing a sequence of security alerts from a Wazuh monitoring system.
    Your only task: 
    decide whether this alert sequence requires mitigation action.
    Consider the sequence and pattern of events, not just individual alerts in isolation.
    Base your decision only on the alert data provided below. Do not assume information that isn't present.
    Output format: {"mitigation_required": True or False, "severity": Low or Medium or High, "reasoning": "one sentence explanation that names the actual events_id or rule_id values from the alert data above that support the decision"}
    """)
    
    human_prompt = HumanMessage(content=str(alerts)) 

    response = structured_llm.invoke([system_prompt, human_prompt])
    print("TRIAGE AGENT RESPONSE:",response, "\n")

    return GraphState(
        session_id=state['session_id'],
        alerts=state['alerts'],
        triage_output={
            "mitigation_required": response.mitigation_required,
            "reasoning": response.reasoning,
            "severity":response.severity
            })
