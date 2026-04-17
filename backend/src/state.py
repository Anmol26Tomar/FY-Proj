from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    query: str
    expanded_queries: List[str]
    retrieved_docs: List[Dict[str, Any]]
    critique_log: str
    draft: str
    verification_errors: List[str]
    revision_count: int
    logs: List[str]
