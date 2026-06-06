from typing import (
    TypedDict,
    Dict,
    List,
    Any,
    Optional
)

from sqlalchemy.orm import Session

class AgentState(TypedDict, total=False):

    # -----------------------------------
    # REQUEST
    # -----------------------------------

    query: str
    session_id: str
    user_id: str
    db: Session

    # -----------------------------------
    # ROUTING
    # -----------------------------------

    intent: str
    secondary_intents: List[str]
    confidence: float

    # -----------------------------------
    # QUERY ANALYSIS
    # -----------------------------------

    filters: Dict[str, Any]
    validation: Dict[str, Any]
    search_payload: Dict[str, Any]

    # -----------------------------------
    # CONTEXT
    # -----------------------------------

    conversation_context: str
    user_preferences: Dict[str, Any]
    context: Dict[str, Any]

    # -----------------------------------
    # VENDOR DATA
    # -----------------------------------

    vendors: List[Dict[str, Any]]
    ranked_vendors: List[Dict[str, Any]]

    # -----------------------------------
    # COMPARISON
    # -----------------------------------

    comparison_result: Dict[str, Any]

    # -----------------------------------
    # RESPONSE
    # -----------------------------------
    ai_response: str

    # -----------------------------------
    # WORKFLOW
    # -----------------------------------

    current_agent: str
    workflow_trace: List[Dict[str, Any]]

    # -----------------------------------
    # ERROR HANDLING
    # -----------------------------------

    errors: List[str]
    retry_count: int