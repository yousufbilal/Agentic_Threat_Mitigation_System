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
   
   print()
   tools = await mcp_client.get_tools()
   print("tools fetched:", len(tools))

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

   system_prompt = SystemMessage(content="""You are a MITRE ATT&CK technique classifier.
        You will be given a sequence of security alerts.

        Your task: identify the single most relevant MITRE ATT&CK technique for this alert sequence, then call the correct tool to retrieve its details.

        Tool selection rules:
        - If you already know the specific technique ID (e.g. T1110), call get_technique_by_id.
        - If you only know the general tactic (e.g. "credential access", "persistence") but not the exact technique, call get_techniques_by_tactic to look up candidates first.

        Only call one tool. Do not guess a technique ID if you are not confident — use get_techniques_by_tactic instead.
        Base your answer only on the alert data given. Do not assume information that isn't present.""")

   tool_prompt = HumanMessage(content=f"Identify the relevant MITRE ATT&CK technique ID for this alert sequence: {alert_log_sequence}")

   ai_msg = await llm_with_tools.ainvoke([tool_prompt])
   print(" LLM responded:", ai_msg.tool_calls)

   if not ai_msg.tool_calls:
       return None

   call = ai_msg.tool_calls[0]
   tool_to_use = tools_by_name[call["name"]]
  
   print("calling tool:", call["name"], call["args"])
   result = await tool_to_use.ainvoke(call["args"])
   print("tool returned:", result)   

   return result