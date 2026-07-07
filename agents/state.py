from typing import TypedDict, List, Dict, Optional

class GraphState(TypedDict):
    alerts: List[Dict]                    # Raw input payload from database
    triage_output: Optional[Dict]         # Agent 1 output (JSON-like dict)
    investigation_output: Optional[Dict]  # Agent 2 output
    review_output: Optional[Dict]         # Agent 3 output
    response_output: Optional[Dict]       # Agent 4 output