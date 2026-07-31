from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState
from pydantic import BaseModel
from typing import Literal
from model_context_protocol.mitre_technique import get_mitre_technique_id
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv() 

class InvestigatorOutput(BaseModel):
    # removed technique as the llm tool call provides is this 
    # attack_technique: str
    affected_entity:str
    summary:str
    cited_rule_ids: list[int]

llm = ChatOllama(model="qwen3:4b", temperature=0)
# llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
structured_llm = llm.with_structured_output(InvestigatorOutput)

async def investigator_agent(state: GraphState) -> GraphState:
    alerts = state["alerts"]
    triage_output = state["triage_output"]
    adversarial_output = state["adversarial_output"]
    alert_log_sequence = state["alert_log_sequence"]

    if adversarial_output is None:
        verdict = None
    else:
        verdict = adversarial_output.get("verdict")

    if verdict == "rejected":
        print(f"Investigator output was {verdict} by Adversarial agent")

    # mitre_technique_id = await get_mitre_technique_id(alert_log_sequence)
    # print("MITRE TECHNIQUE RESULT:", mitre_technique_id)

    mitre_mcp_tool_result = await get_mitre_technique_id(alert_log_sequence)

    if verdict == "rejected":
        system_prompt = SystemMessage(content="""You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.
            Your only task:
            identify the likely attack technique or pattern in this alert sequence, and which account or host it affects.
            Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.

            If a previous_critique is included below, it means an adversarial reviewer rejected your prior conclusion. Read the
            reviewer's technique_judgment and entity_judgment carefully, and produce a revised attack_technique and/or
            affected_entity that directly addresses the reviewer's stated concerns. Do not repeat your previous answer unchanged.

            Output format: {"affected_entity": "account/host from the data",
            "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion]}
            Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs.""")
        payload = {"alerts": alerts, "triage_output": triage_output, "adversarial_output": adversarial_output}
    else:
        system_prompt = SystemMessage(content="""You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.
            Your only task:
            identify the likely attack technique or pattern in this alert sequence, and which account or host it affects.
            Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.
            Output format: {"affected_entity": "account/host from the data",
            "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion]}
            Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs.""")
        payload = {"alerts": alerts, "triage_output": triage_output}

    human_prompt = HumanMessage(content=str(payload))

    response = await structured_llm.ainvoke([system_prompt, human_prompt])
    print()
    print("INVESTIGATOR AGENT RESPONSE:", response, "MCP TOOL CALL RESULT:", mitre_mcp_tool_result, "\n")
    print()

    if mitre_mcp_tool_result is not None:
        attack_technique = mitre_mcp_tool_result.technique_name
        technique_id = mitre_mcp_tool_result.technique_id
    else:
        attack_technique = None
        technique_id = None

    return GraphState(
        session_id=state['session_id'],
        alerts=state["alerts"],
        investigator_output={
            "attack_technique": attack_technique,
            "technique_id": technique_id,
            "affected_entity": response.affected_entity,
            "cited_rule_ids": response.cited_rule_ids,
            "summary": response.summary,
        })
