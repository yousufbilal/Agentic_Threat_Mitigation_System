from langchain_ollama import ChatOllama  
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GraphState  
from pydantic import BaseModel
from typing import Literal, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv() 

class AdversalOutput(BaseModel):
    verdict: Literal["confirmed", "rejected"]
    technique_judgment: str
    entity_judgment: str
    cited_rule_ids: list[int]
    # revised_technique: Optional[str] = None
    # revised_entity: Optional[str] = None

# llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0, reasoning=True)
# llm = ChatOllama(model="qwen3:4b", temperature=0, reasoning=True)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

structured_llm = llm.with_structured_output(AdversalOutput)

def adversarial_agent(state: GraphState) -> GraphState:

    alerts = state["alerts"]
    investigator_output = state["investigator_output"]
    # triage_output = state["triage_output"]

    revision_count = state["revision_count"]

    system_prompt = SystemMessage(content="""
        You are a SOC adversarial reviewer. Independently judge whether the Investigator's attack_technique
        and affected_entity are each supported by the alert data.

        Reject if either:
        - is not backed by the cited alerts
        - ignores a more likely explanation (e.g. false positive, benign admin activity)
        - affected_entity is a generic placeholder (e.g. "host", "account") instead of a real value

        Otherwise confirm.

        Output format: {
        "verdict": "confirmed" or "rejected",
        "technique_judgment": "one sentence on whether the cited rule_ids support the technique",
        "entity_judgment": "one sentence on whether the cited rule_ids support the entity",
        "cited_rule_ids": [rule_id values from the alert data that directly support your judgments]
        }
        Only include rule_id values that literally appear in the alert data below. Do not invent or guess IDs.
        """)
    
    human_prompt = HumanMessage(content=str({"alerts": alerts, "investigator_output": investigator_output, }))

    # COT LOGIC 
    # reasoning = llm.invoke([system_prompt, human_prompt])
    # cot = reasoning.additional_kwargs.get("reasoning_content")
    # print("ADVERSAL AGENT REASONING (CoT):", cot)

    response = structured_llm.invoke([system_prompt, human_prompt])
    print()
    print("ADVERSAL AGENT RESPONSE:",response, "\n")
    print()
    
    adversal_verdict = response.verdict
    
    if adversal_verdict == "rejected":
        revision_count += 1

    return GraphState(
        adversarial_output={
            "verdict": response.verdict,
            # "revised_technique": response.revised_technique,
            # "revised_entity": response.revised_entity,
            "technique_judgment": response.technique_judgment,
            "entity_judgment": response.entity_judgment,
            "cited_rule_ids": response.cited_rule_ids
        },
                revision_count = revision_count
    )