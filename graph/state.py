from typing import TypedDict, List, Dict, Optional
from sympy import limit
from typing import Annotated, List, Literal, TypedDict
import operator

class GraphState(TypedDict):
    # session_id: str
    # alerts: List[dict]
    # triage_output: Optional[dict]
    nlist:Annotated[list[str], operator.add] 
