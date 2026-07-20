from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from pydantic import BaseModel
from typing import Literal

class ResponderOutput(BaseModel):
    alert_ids: list[str]
    affected_asset: str
    action: Literal["escalate", "contain", "monitor", "dismiss"]
    severity: Literal["low", "medium", "high", "critical"]
    confidence: float
    justification: str
    remediation_plan: str    

llm = ChatOllama(model="qwen2.5:3b", temperature=0)

structured_llm = llm.with_structured_output(ResponderOutput)


def responder_agent(state: GraphState) -> GraphState:

    # session_id=state['session_id']

    alerts= state["alerts"],

    investigator_output = state["investigator_output"]
    adversarial_output = state["adversarial_output"]

    system_prompt = SystemMessage(content="""You are a SOC responder deciding the mitigation action for a security alert sequence.
        Your only task:
        Based on the adversarial reviewer's verdict decide the mitigation action, severity, and remediation plan.

        Base your decision only on the data provided below. Do not assume information that isn't present.

        Output format:
        {
            "action": "escalate" | "contain" | "monitor" | "dismiss",
            "target": "affected account/host",
            "severity": "low" | "medium" | "high" | "critical",
            "confidence": float between 0 and 1,
            "justification": "one to two sentence explanation referencing the verdict and technique",
            "remediation_plan": "concrete steps to take, e.g. isolate host, disable account, block IP, reset credentials"
        }
        """)

    # human_prompt = HumanMessage(content=str({"investigator_output": investigator_output, "adversarial_output": adversarial_output}))
    human_prompt = HumanMessage(content=str({
        "adversarial_output": adversarial_output,
        "alerts": alerts,
    }))

    response = structured_llm.invoke([system_prompt, human_prompt])
    
    print("REPONDER AGENT RESPONSE:",response, "\n")

    return GraphState(
        responder_output={
            "alert_ids": response.alert_ids,
            "affected_asset": response.affected_asset,
            "action": response.action,
            "severity": response.severity,
            "confidence": response.confidence,
            "justification": response.justification,
            "remediation_plan": response.remediation_plan
        }
    )