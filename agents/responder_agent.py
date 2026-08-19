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
from langchain_groq import ChatGroq
from model_context_protocol.mitre_mitigation import get_mitre_mitigation
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# all other pydantic classes do not have field description look into it further 
class ResponderOutput(BaseModel):
    action: Literal["escalate", "contain", "monitor"]
    severity: Literal["low", "medium", "high", "critical"]
    confidence: float
    mitigation_names: list[str] = Field(description="MITRE mitigation names corresponding to mitigation_ids")
    mitigation_descriptions: list[str] = Field(description="MITRE mitigation descriptions corresponding to mitigation_ids")
    reasoning: str = Field(description="One to two sentences explaining the decision")
    remediation_plan: str = Field(description="Numbered list of concrete steps")

# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0, reasoning=True)
# llm = ChatOllama(model="qwen3:4b", temperature=0, reasoning=True)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
# MODEL_NAME = "groq-llama-3.3-70b-versatile"
# llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


# MODEL_NAME = "qwen2.5-3b"
# llm = ChatOllama(model="qwen2.5:3b", temperature=0)

# MODEL_NAME = "qwen3:4b"
# llm = ChatOllama(model="qwen3:4b", temperature=0)

MODEL_NAME = "gemini-3.7-flash"
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0)


structured_llm = llm.with_structured_output(ResponderOutput)
os.makedirs("agent_outputs", exist_ok=True)   



async def responder_agent(state: GraphState) -> GraphState:

    start_time = time.time()

    adversarial_output = state["adversarial_output"]
    session_id = state["session_id"]
    domain = state["investigator_output"]["domain"]
    cited_rule_ids = state["adversarial_output"]["cited_rule_ids"]
    session_id = state["triage_output"]["session_id"]
    technique_id = state["adversarial_output"]["technique_id"]
    technique_name = state["adversarial_output"]["technique_name"]
    cited_rule_ids = state["adversarial_output"]["cited_rule_ids"]
    
    # bug the adversarial agent output does not contain the mitre attack technique ID or Name 
    # check to make sure i am only sending 1 query to the agetic rag tool and not multiple queries

    # print("THIS IS THE MITIGATION TOOL",mitigation_data)
    file_path = Path(f"mitre_mitigations/mitre_mitigations_{domain}.json")

    if not file_path:
        mitigation_domain = await get_mitre_mitigation(domain)

    mitigation_data = await run_agent(adversarial_output, domain)
    print()
    print("THIS IS MITIGATION DATA FROM RUN AGENT ",mitigation_data)
    print()

    system_prompt = SystemMessage(content="""
        You are a SOC responder deciding the mitigation action for a security alert sequence.

        Your only task:
        Based on the adversarial reviewer's verdict and the retrieved_mitigation_data, decide the action and remediation plan and confidence and provide your reasoning.
        Base your decision only on the data provided below. Do not assume information that isn't present.

        IMPORTANT: Your remediation_plan must be grounded in the retrieved_mitigation_data provided and use to to fill the mitigation details in output
        Write the remediation_plan as a clear, numbered list of concrete steps a SOC analyst can act on immediately. 
        Keep each step short and actionable. use
        
        Output format:
        {
            "action": "escalate" | "contain" | "monitor",
            "severity": "low" | "medium" | "high" | "critical",
            "confidence": float between 0 and 1,
            "reasoning": "explanation referencing the verdict and technique",
            "mitigation_names": "list of mitigation names corresponding to the mitigation_ids used",
            "mitigation_descriptions": "list of mitigation descriptions corresponding to the mitigation_ids used",
            "remediation_plan": "numbered list of concrete steps, filtered to only what's relevant, grounded in retrieved_mitigation_data and adversarial_output"
        }
        """)

    human_prompt = HumanMessage(content=str({
        "adversarial_output": adversarial_output,
        "domain": domain,
        "retrieved_mitigation_data": mitigation_data,
    }))

    response = structured_llm.invoke([system_prompt, human_prompt])
    end_time = time.time()
    agent_execution_time = end_time - start_time
    print(f"Responder Agent Response Time: {agent_execution_time:.2f} seconds")
    print()
    print("REPONDER AGENT RESPONSE:",response, "\n")
    print()

    decision = interrupt({"responder_output": response})

    if decision == "y":
        responder_output = {
            "username": state["adversarial_output"]["affected_account"],
            "hostname": state["adversarial_output"]["affected_host"],
            "ip": state["adversarial_output"]["affected_ip"],
            "agent_id": state["adversarial_output"]["agent_id"],
            "technique_id": technique_id,
            "technique_name": technique_name,
            "cited_rule_ids": cited_rule_ids,
            "mitigation_names": response.mitigation_names,
            "mitigation_descriptions": response.mitigation_descriptions,
            "action": response.action,
            "severity": response.severity,
            "confidence": response.confidence,
            "reasoning": response.reasoning,
            "remediation_plan": response.remediation_plan
        }

        os.makedirs(f"responder_output/{MODEL_NAME}", exist_ok=True)
        with open(f"responder_output/{MODEL_NAME}/{session_id}_result.json", "w") as file:
            json.dump(responder_output, file, indent=2)

        print(f"Human decision: {decision}")

        return GraphState(responder_output=responder_output)
    else:
        return GraphState(responder_output=None)
