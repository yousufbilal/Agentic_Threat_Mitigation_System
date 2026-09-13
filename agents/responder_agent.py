from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from pydantic import BaseModel, Field
from typing import Literal
import asyncio
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import time
from dotenv import load_dotenv
load_dotenv()

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

    session_id = state["triage_output"]["session_id"]

    # adversarial 
    adversarial_output = state["adversarial_output"]
    cited_rule_ids = state["adversarial_output"]["cited_rule_ids"]
    technique_name = state["adversarial_output"]["technique_name"]
    technique_id = state["adversarial_output"]["technique_id"]


    # Investigator 
    investigator_output = state["investigator_output"]
    domain = state["investigator_output"]["domain"]
    # cited_rule_ids = state["investigator_output"]["cited_rule_ids"]
    # Technique ID and Name from investigator output
    # technique_id = state["investigator_output"]["technique_id"]
    # technique_name = state["investigator_output"]["technique_name"]


    system_prompt = SystemMessage(content="""
        You are a SOC responder deciding the mitigation action for a security alert sequence.

        Your only task:
        Based on the adversarial reviewer's findings, use your own knowledge of MITRE ATT&CK mitigations to decide the action and remediation plan, confidence, and provide your reasoning.
        Base your decision only on the data provided below. Do not assume information that isn't present.

        IMPORTANT: Your remediation_plan must fill in the mitigation details in the output.
        Write the remediation_plan as a clear, numbered list of concrete steps a SOC analyst can act on immediately.
        Keep each step short and actionable.

        Output format:
        {
            "action": "escalate" | "contain" | "monitor",
            "severity": "low" | "medium" | "high" | "critical",
            "confidence": float between 0 and 1,
            "reasoning": "explanation referencing the adversarial reviewer's findings and technique",
            "mitigation_names": "list of MITRE ATT&CK mitigation names",
            "mitigation_descriptions": "list of mitigation descriptions corresponding to the mitigation names",
            "remediation_plan": "numbered list of concrete steps, filtered to only what's relevant, grounded in adversarial_output and your own knowledge of the identified technique"
        }
        """)



    human_prompt = HumanMessage(content=str({
        "adversarial_output": adversarial_output,
        "domain": domain,
        # "investigator_output": investigator_output,
    }))

    response = structured_llm.invoke([system_prompt, human_prompt])
    end_time = time.time()
    agent_execution_time = end_time - start_time
    print(f"Responder Agent Response Time: {agent_execution_time:.2f} seconds")
    print()
    print("REPONDER AGENT RESPONSE:",response, "\n")
    print()


    responder_output = {
        "username": state["adversarial_output"]["affected_account"],
        "hostname": state["adversarial_output"]["affected_host"],
        "ip": state["adversarial_output"]["affected_ip"],
        "agent_id": state["adversarial_output"]["agent_id"],
        # "username": state["investigator_output"]["affected_account"],
        # "hostname": state["investigator_output"]["affected_host"],
        # "ip": state["investigator_output"]["affected_ip"],
        # "agent_id": state["investigator_output"]["agent_id"],
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


    return GraphState(responder_output=responder_output)
