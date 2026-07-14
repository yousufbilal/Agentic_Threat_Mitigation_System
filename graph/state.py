from typing import TypedDict, List, Dict, Optional, Annotated, Literal
import operator

class GraphState(TypedDict):
    session_id: str
    alerts: List[dict]
    triage_output: Optional[dict]
    investigator_output: Optional[dict]
