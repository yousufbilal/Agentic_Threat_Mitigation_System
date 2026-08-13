from botocore import response
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
from model_context_protocol.mitre_mitigation import get_mitre_mitigation
from dotenv import load_dotenv
load_dotenv() 

# all other pydantic classes do not have field description look into it further 
class ResponderOutput(BaseModel):
    # alert_ids: list[str] = Field(description="List of alert IDs involved in this incident")
    # affected_asset: str = Field(description="Format: 'username @ hostname (ip_address, agent_id)'. Example: 'phopkins @ intranet-server (10.35.35.206, agent 27)'. NOT severity, NOT a plan, NOT a sentence.")
    # action: Literal["escalate", "contain", "monitor", "dismiss"]
    # severity: Literal["low", "medium", "high", "critical"]
    action: Literal["escalate", "contain", "monitor"]
    # domain: Literal["enterprise-attack", "mobile-attack", "ics-attack"]
    confidence: float
    reasoning: str = Field(description="One to two sentences explaining the decision")
    remediation_plan: str = Field(description="Numbered list of concrete steps") 

# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0, reasoning=True)
# llm = ChatOllama(model="qwen3:4b", temperature=0, reasoning=True)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
structured_llm = llm.with_structured_output(ResponderOutput)
os.makedirs("agent_outputs", exist_ok=True)   



async def responder_agent(state: GraphState) -> GraphState:

    alerts= state["alerts"]
    adversarial_output = state["adversarial_output"]
    session_id = state["session_id"]
    domain = state["investigator_output"]["domain"]


    print("RESPONDER DOMAIN IS ",domain)
    
    # bug the adversarial agent output does not contain the mitre attack technique ID or Name 
    # check to make sure i am only sending 1 query to the agetic rag tool and not multiple queries


    # print("THIS IS THE MITIGATION TOOL",mitigation_data)
    mitigation_domain = await get_mitre_mitigation(domain)

    mitigation_data = await run_agent(f"Find a mitigation for this attack: {adversarial_output}", domain )
    

    system_prompt = SystemMessage(content="""
        You are a SOC responder deciding the mitigation action for a security alert sequence.

        Your only task:
        Based on the adversarial reviewer's verdict and the retrieved_mitigation_data, decide the action and remediation plan and confidence and provide your reasoning.
        Base your decision only on the data provided below. Do not assume information that isn't present.

        IMPORTANT: Your remediation_plan must be grounded in the retrieved_mitigation_data provided.
        Write the remediation_plan as a clear, numbered list of concrete steps a SOC analyst can act on immediately. 
        Keep each step short and actionable.
        
        Output format:
        {  
            "action": "escalate" | "contain" | "monitor",
            "confidence": float between 0 and 1,
            "reasoning": "explanation referencing the verdict and technique",
            "remediation_plan": "numbered list of concrete steps, filtered to only what's relevant, grounded in retrieved_mitigation_data and adversarial_output"
        }
        """)

    human_prompt = HumanMessage(content=str({
        "adversarial_output": adversarial_output,
        "alerts": alerts,
        # "retrieved_mitigation_data": mitigation_data,
    }))

    response = structured_llm.invoke([system_prompt, human_prompt])
    print()
    print("REPONDER AGENT RESPONSE:",response, "\n")
    print()

    decision = interrupt({"responder_output": response})

    if decision == "y":
        with open(f"deepseek_output/{session_id}_result.json", "w") as file:
            json.dump(response.model_dump(), file, indent=2)
        print(f"Human decision: {decision}")
        return GraphState(
            responder_output={
                # "alert_ids": response.alert_ids,
                # "affected_asset": response.affected_asset,
                "action": response.action,
                # "severity": response.severity,
                "confidence": response.confidence,
                "reasoning": response.reasoning,
                "remediation_plan": response.remediation_plan
            }
        )
    else:
        return GraphState(responder_output=None)
