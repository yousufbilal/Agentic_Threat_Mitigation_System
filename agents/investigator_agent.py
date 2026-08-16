from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState
from pydantic import BaseModel
from typing import Literal
from model_context_protocol.mitre_technique import get_mitre_technique_id
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
# from model_context_protocol.agentic_rag import run_agent
from dotenv import load_dotenv
load_dotenv()

class InvestigatorOutput(BaseModel):
    # removed technique as the llm tool call provides is this
    # attack_technique: str
    affected_account: str     
    affected_host: str         
    affected_ip: str           
    agent_id: str               
    cited_rule_ids: list[int]
    domain: Literal["enterprise-attack", "mobile-attack", "ics-attack"]
    reasoning: str

# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0)
# llm = ChatOllama(model="qwen3:4b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)
# MODEL_NAME = "groq-llama-3.3-70b-versatile"
# llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
MODEL_NAME = "qwen2.5-3b"
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
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

#   need to check as this utility agent does not know if adversaial agent rejeted the outpout and if it needs to revise 
    mitre_mcp_tool_result = await get_mitre_technique_id(alert_log_sequence) 
# confusing name change them so its much clear what tool i am using and what the result is
    # this model only provide full list of mitre techniques
    # this is the mitiagtion tool that im supplying the log sequence to 

    # print()
    # print("MITRE TECHNIQUE RESULT:", mitre_mcp_tool_result, "\n")
    # print()

    if verdict == "rejected":
        system_prompt = SystemMessage(content="""
            You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.

            Task: identify the specific account or host affected by this alert sequence.
            An attack_technique is included in the data below — use it as context when reasoning about which entity it affects.

            A previous_critique is included below — an adversarial reviewer rejected your prior conclusion. Read
            entity_judgment carefully and produce a revised affected_entity that directly addresses the reviewer's
            stated concerns. Do not repeat your previous answer unchanged.

            Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.
            Only include rule_id values that appear in the alert data below. Do not invent or guess IDs.

            Output format: {
            "affected_account": "the account/username involved, e.g. 'phopkins'",
            "affected_host": "the hostname involved, e.g. 'intranet-server'",
            "affected_ip": "the IP address involved, e.g. '10.35.35.206'",
            "agent_id": "the Wazuh agent ID if present in the alert data, e.g. '27'",
            "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion],
            "domain": "enterprise-attack" | "mobile-attack" | "ics-attack",
            "reasoning": "explanation of why this entity was identified as the affected account/host, based on the alert data and the given technique"
            }""")
        payload = {
            "alerts": alerts,
            "triage_output": triage_output,
            "adversarial_output": adversarial_output,
            "attack_technique": mitre_mcp_tool_result.technique_name if mitre_mcp_tool_result else None,
            "technique_id": mitre_mcp_tool_result.technique_id if mitre_mcp_tool_result else None
        }

    else:
        system_prompt = SystemMessage(content="""
            You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.

            Task: identify the specific account or host affected by this alert sequence.
            An attack_technique is included in the data below — use it as context when reasoning about which entity it affects.

            Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.
            Only include rule_id values that appear in the alert data below. Do not invent or guess IDs.

            Output format: {
            "affected_account": "the account/username involved, e.g. 'phopkins'",
            "affected_host": "the hostname involved, e.g. 'intranet-server'",
            "affected_ip": "the IP address involved, e.g. '10.35.35.206'",
            "agent_id": "the Wazuh agent ID if present in the alert data, e.g. '27'",
            "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion],
            "domain": "enterprise-attack" | "mobile-attack" | "ics-attack",
            "reasoning": "explanation of why this entity was identified as the affected account/host, based on the alert data and the given technique"
            }""")
        
        payload = {
            "alerts": alerts,
            "triage_output": triage_output,
            "attack_technique": mitre_mcp_tool_result.technique_name if mitre_mcp_tool_result else None,
            "technique_id": mitre_mcp_tool_result.technique_id if mitre_mcp_tool_result else None
        }

        
    human_prompt = HumanMessage(content=str(payload))

    response = await structured_llm.ainvoke([system_prompt, human_prompt])
    print()
    # print("INVESTIGATOR AGENT RESPONSE:", response, "MCP TOOL CALL RESULT:", mitre_mcp_tool_result, "\n")
    print("INVESTIGATOR AGENT RESPONSE:", response)
    print()

#   need to check as this utility agent does not know if adversaial agent rejeted the outpout and if it needs to revise 

    # mitigation_data = await run_agent(f"Find a mitigation for this attack: {adversarial_output}", response.domain )


    if mitre_mcp_tool_result is not None:
        attack_technique = mitre_mcp_tool_result.technique_name
        technique_id = mitre_mcp_tool_result.technique_id
    else:
        attack_technique = None
        technique_id = None

    return GraphState(
        investigator_output={
            "affected_account": response.affected_account,
            "affected_host": response.affected_host,
            "affected_ip": response.affected_ip,
            "agent_id": response.agent_id,
            "cited_rule_ids": response.cited_rule_ids,
            "reasoning": response.reasoning,
            "attack_technique": attack_technique,
            "technique_id": technique_id,
            "domain": response.domain
        })
