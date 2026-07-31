from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from pydantic import BaseModel, Field
from typing import Literal
from langgraph.types import interrupt
from model_context_protocol.agentic_rag import run_agent
import asyncio
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv() 

class ResponderOutput(BaseModel):
    alert_ids: list[str] = Field(description="List of alert IDs involved in this incident")
    affected_asset: str = Field(description="Format: 'username @ hostname (ip_address, agent_id)'. Example: 'phopkins @ intranet-server (10.35.35.206, agent 27)'. NOT severity, NOT a plan, NOT a sentence.")
    action: Literal["escalate", "contain", "monitor", "dismiss"]
    severity: Literal["low", "medium", "high", "critical"]
    confidence: float
    justification: str = Field(description="One to two sentences explaining the decision")
    remediation_plan: str = Field(description="Numbered list of concrete steps") 

llm = ChatOllama(model="qwen3:4b", temperature=0, reasoning=True)
# llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
structured_llm = llm.with_structured_output(ResponderOutput)
os.makedirs("agent_outputs", exist_ok=True)   



async def responder_agent(state: GraphState) -> GraphState:

    alerts= state["alerts"]
    adversarial_output = state["adversarial_output"]
    session_id = state["session_id"]

    mitigation_data = await run_agent(f"Find a mitigation for this attack: {adversarial_output}")
    print("THIS IS THE MITIGATION TOOL",mitigation_data)

    system_prompt = SystemMessage(content="""You are a SOC responder deciding the mitigation action for a security alert sequence.
        Your only task:
        Based on the adversarial reviewer's verdict and the retrieved_mitigation_data, decide the mitigation action, severity, and remediation plan.
        Base your decision only on the data provided below. Do not assume information that isn't present.
        IMPORTANT: Your remediation_plan must be grounded in the retrieved_mitigation_data provided.
        Write the remediation_plan as a clear, numbered list of concrete steps a SOC analyst can act on immediately. Remove any HTML tags or citation references from the retrieved data before including them. Keep each step short and actionable.
        Output format:
        {
            "action": "escalate" | "contain" | "monitor" | "dismiss",
            "affected_asset": "affected account/host in the format 'username @ hostname (ip_address, agent_id)', e.g. 'phopkins @ intranet-server (10.35.35.206, agent 27)'",            
            "severity": "low" | "medium" | "high" | "critical",
            "confidence": float between 0 and 1,
            "justification": "one to two sentence explanation referencing the verdict and technique",
            "remediation_plan": "numbered list of concrete steps, filtered to only what's relevant, grounded in retrieved_mitigation_data and adversarial_output"
        }

        Example output:
        {
            "action": "contain",
            "affected_asset": "phopkins @ intranet-server (10.35.35.206, agent 27)",
            "severity": "critical",
            "confidence": 0.95,
            "justification": "Root access confirmed via sudo, /etc/shadow was read.",
            "remediation_plan": "1. Isolate host. 2. Lock account. 3. Rotate credentials."
        }
        """)

    human_prompt = HumanMessage(content=str({
        "adversarial_output": adversarial_output,
        "alerts": alerts,
        "retrieved_mitigation_data": mitigation_data,
    }))

    response = structured_llm.invoke([system_prompt, human_prompt])
    print()
    print("REPONDER AGENT RESPONSE:",response, "\n")
    print()

    decision = interrupt({"responder_output": response})

    if decision == "y":
        with open(f"qwen3:4b_output/{session_id}_result.json", "w") as file:
            json.dump(response.model_dump(), file, indent=2)
        print(f"Human decision: {decision}")
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
    else:
        return GraphState(responder_output=None)
