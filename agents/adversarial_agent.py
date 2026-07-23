from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from pydantic import BaseModel
from typing import Literal, Optional

class AdversalOutput(BaseModel):
    # verdict: Literal["confirmed", "revised", "rejected"]
    verdict: Literal["rejected"]
    technique_judgment: str
    entity_judgment: str
    cited_rule_ids: list[int]
    revised_technique: Literal[
    "network_scans", "service_scans", "dirb", "wpscan", "webshell",
    "cracking", "reverse_shell", "privilege_escalation",
    "service_stop", "dnsteal", "other", "none"]
    revised_entity: Optional[str] = None

llm = ChatOllama(model="qwen2.5:3b", temperature=0)
structured_llm = llm.with_structured_output(AdversalOutput)

def adversarial_agent(state: GraphState) -> GraphState:

    alerts = state["alerts"]
    investigator_output = state["investigator_output"]
    triage_output = state["triage_output"]
    revision_count = state["revision_count"]

    system_prompt = SystemMessage(content="""You are a SOC adversarial reviewer challenging an investigator's conclusion about a security alert sequence.
        Your task: independently judge whether attack_technique and affected_entity are EACH supported by the alert data, or whether either
        overreaches, ignores an alternative explanation (e.g. false positive, benign admin activity), or is not backed by the cited events.
        Base your review only on the alert data, triage reasoning, and investigator output provided below. Do not assume information that isn't present.

        If affected_entity contains generic placeholder text instead of a specific value (e.g. the literal word "host" or "account" with no
        actual hostname/username resolved), treat that as NOT supported and set entity_verdict to "revised" with a corrected value, or "rejected"
        if no specific entity can be determined from the alert data.
        
        Output format: {"technique_verdict":"rejected",
                                  
        "entity_verdict": "confirmed" or "revised" or "rejected",
        "revised_technique": "short label, required if technique_verdict is revised, otherwise null",
        "revised_entity": "corrected account/host, required if entity_verdict is revised, otherwise null",
        "technique_judgment": "one sentence stating what the cited rule_id values' actual content shows and why it does or doesn't support the technique",
        "entity_judgment": "one sentence stating what the cited rule_id values' actual content shows and why it does or doesn't support the entity",
        "cited_rule_ids": [rule_id values from the alert data above that directly support your judgments]}
        Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs. ]}""")

    # human_prompt = HumanMessage(content=str({"alerts": alerts, "investigator_output": investigator_output, "triage_output": triage_output}))
    human_prompt = HumanMessage(content=str({"alerts": alerts, "investigator_output": investigator_output, }))

    response = structured_llm.invoke([system_prompt, human_prompt])
    
    print("ADVERSAL AGENT RESPONSE:",response, "\n")

    adversal_verdict = response.verdict
    
    if adversal_verdict == "rejected":
        revision_count += 1

    return GraphState(
        adversarial_output={
            "verdict": response.verdict,
            "revised_technique": response.revised_technique,
            "revised_entity": response.revised_entity,
            "technique_judgment": response.technique_judgment,
            "entity_judgment": response.entity_judgment,
            "cited_rule_ids": response.cited_rule_ids
        },
                revision_count = revision_count
    )