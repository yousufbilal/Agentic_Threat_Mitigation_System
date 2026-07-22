from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from pydantic import BaseModel
from typing import Literal
from mcp_tools.mcp_client import mcp_client

class InvestigatorOutput(BaseModel):
    attack_technique: Literal[
        "network_scans",
        "service_scans",
        "dirb",
        "wpscan",
        "webshell",
        "cracking",
        "reverse_shell",
        "privilege_escalation",
        "service_stop",
        "dnsteal",
        "other"]
    affected_entity:str
    summary:str
    cited_rule_ids: list[int]


llm = ChatOllama(model="qwen2.5:3b", temperature=0)
structured_llm = llm.with_structured_output(InvestigatorOutput)

async def investigator_agent(state:GraphState)-> GraphState:

    # revision_count = state["revision_count"]
    alerts = state["alerts"]
    triage_output = state["triage_output"]
    adversarial_output = state["adversarial_output"]

#   this was aded manually these are the tools we will focus on 
    allowed_tool_names = (
        "get_technique_by_id",
        "get_techniques_by_tactic",
    )

    tools = await mcp_client.get_tools()


    filtered_tools = []
    for t in tools:
        if t.name in allowed_tool_names:
            filtered_tools.append(t)


    if adversarial_output is not None:
        verdict = adversarial_output.get("verdict")
    else:
        verdict = None

    if verdict == "rejected":
        print(f"Investigator output was {verdict} by Adversarial agent")        
        return investigator_agent_loop_review(state)

    system_prompt = SystemMessage(content="""You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.
        Your only task:
        identify the likely attack technique or pattern in this alert sequence, and which account or host it affects.
        Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.
        Output format: {"attack_technique": "short label", "affected_entity": "account/host from the data",
        "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion]}
        Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs.""")

    human_prompt = HumanMessage(content=str({"alerts": alerts, "triage_output": triage_output}))

    response = structured_llm.invoke([system_prompt, human_prompt])

    print("INVESTIGATOR AGENT RESPONSE:",response, "\n")

    return GraphState(
        
        session_id=state['session_id'],

        alerts= state["alerts"],

        investigator_output={
            "attack_technique": response.attack_technique,
            "affected_entity": response.affected_entity,
            "cited_rule_ids": response.cited_rule_ids,
            "summary": response.summary,
            })


def investigator_agent_loop_review(state: GraphState):
    adversarial_output = state["adversarial_output"]
    alerts = state["alerts"]
    triage_output = state["triage_output"]

    system_prompt = SystemMessage(content="""You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.
        Your only task:
        identify the likely attack technique or pattern in this alert sequence, and which account or host it affects.
        Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.

        If a previous_critique is included below, it means an adversarial reviewer rejected your prior conclusion. Read the
        reviewer's technique_judgment and entity_judgment carefully, and produce a revised attack_technique and/or
        affected_entity that directly addresses the reviewer's stated concerns. Do not repeat your previous answer unchanged.

        Output format: {"attack_technique": "short label", "affected_entity": "account/host from the data",
        "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion]}
        Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs.""")

    human_prompt = HumanMessage(content=str({"alerts": alerts, "triage_output": triage_output, "adversarial_output": adversarial_output}))
    response = structured_llm.invoke([system_prompt, human_prompt])
        
    print("REVISED INVESTIGATOR AGENT RESPONSE:",response, "\n")

    return GraphState(
        
            session_id=state['session_id'],

            alerts= state["alerts"],

            investigator_output={
                "attack_technique": response.attack_technique,
                "affected_entity": response.affected_entity,
                "cited_rule_ids": response.cited_rule_ids,
                "summary": response.summary,
                })




