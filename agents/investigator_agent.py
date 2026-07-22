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

async def get_mitre_technique_id(alert_log_sequence):
   print("1. fetching tools...")
   tools = await mcp_client.get_tools()
   print("2. tools fetched:", len(tools))

   allowed_tool_names = (
       "get_technique_by_id",
       "get_techniques_by_tactic",
   )

   tools_by_name = {}
   for tool in tools:
       if tool.name in allowed_tool_names:
           tools_by_name[tool.name] = tool

   filtered_tools = list(tools_by_name.values())

   llm_with_tools = llm.bind_tools(filtered_tools)

   tool_prompt = HumanMessage(content=f"Identify the relevant MITRE ATT&CK technique ID for this alert sequence: {alert_log_sequence}")


   print("3. asking LLM to pick a tool...")
   ai_msg = await llm_with_tools.ainvoke([tool_prompt])
   print("4. LLM responded:", ai_msg.tool_calls)

   if not ai_msg.tool_calls:
       return None

   call = ai_msg.tool_calls[0]
   tool_to_use = tools_by_name[call["name"]]
  
   print("5. calling tool:", call["name"], call["args"])
   result = await tool_to_use.ainvoke(call["args"])
   print("6. tool returned:", result)   

   return result


async def investigator_agent(state:GraphState)-> GraphState:
    alerts = state["alerts"]
    triage_output = state["triage_output"]
    adversarial_output = state["adversarial_output"]
    alert_log_sequence = state["alert_log_sequence"]


    if adversarial_output is not None:
        verdict = adversarial_output.get("verdict")
    else:
        verdict = None

    if verdict == "rejected":
        print(f"Investigator output was {verdict} by Adversarial agent")
        return await investigator_agent_loop_review(state)

    mitre_technique_id = await get_mitre_technique_id(alert_log_sequence)
    print("MITRE TECHNIQUE RESULT:", mitre_technique_id)


    system_prompt = SystemMessage(content="""You are a SOC investigator reviewing a sequence of security alerts that have been flagged for mitigation.
        Your only task:
        identify the likely attack technique or pattern in this alert sequence, and which account or host it affects.
        Base your analysis only on the alert data and triage reasoning provided below. Do not assume information that isn't present.
        Output format: {"attack_technique": "short label", "affected_entity": "account/host from the data",
        "cited_rule_ids": [list of rule_id values from the alert data above that directly support your conclusion]}
        Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs.""")

    human_prompt = HumanMessage(content=str({"alerts": alerts, "triage_output": triage_output}))

    response =  await structured_llm.ainvoke([system_prompt, human_prompt])

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


# same as investigator_agent but re-runs with adversarial feedback included, after a rejected verdict
async def investigator_agent_loop_review(state: GraphState):
    adversarial_output = state["adversarial_output"]
    alerts = state["alerts"]
    triage_output = state["triage_output"]
    alert_log_sequence = state["alert_log_sequence"]

    mitre_technique_id = await get_mitre_technique_id(alert_log_sequence)
    print("MITRE TECHNIQUE RESULT:", mitre_technique_id)


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
    response =  await structured_llm.ainvoke([system_prompt, human_prompt])

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
