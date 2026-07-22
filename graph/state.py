from typing import TypedDict, List, Dict, Optional, Annotated, Literal
import operator

class GraphState(TypedDict):
    session_id: str
    alerts: List[dict]
    alert_log_sequence: list[dict]
    triage_output: Optional[dict]
    investigator_output: Optional[dict]
    adversarial_output: Optional[dict]
    responder_output: Optional[dict]
    revision_count: int
    human_decision: str 

