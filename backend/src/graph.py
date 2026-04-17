from langgraph.graph import StateGraph, END
from .state import AgentState
from .agents import librarian_node, skeptic_node, synthesizer_node, supervisor_node

def verify_routing(state: AgentState) -> str:
    """The conditional routing logic mimicking the hallucination guard."""
    errors = state.get("verification_errors", [])
    rev_count = state.get("revision_count", 0)
    
    # If the Supervisor caught errors, and we haven't looped too many times, go back to drafting
    if len(errors) > 0 and rev_count < 3:
        return "synthesizer"
    
    # Otherwise, it's verified or we maxed out revisions
    return "end"

def build_graph():
    """Compiles the Scholar-Agent Multi-Agent Orchestration architecture."""
    workflow = StateGraph(AgentState)
    
    # 1. Add specialized nodes
    workflow.add_node("librarian", librarian_node)
    workflow.add_node("skeptic", skeptic_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("supervisor", supervisor_node)
    
    # 2. Define the exact linear DAG structure from design spec
    workflow.set_entry_point("librarian")
    workflow.add_edge("librarian", "skeptic")
    workflow.add_edge("skeptic", "synthesizer")
    workflow.add_edge("synthesizer", "supervisor")
    
    # 3. Add the cyclic feedback loop
    workflow.add_conditional_edges(
        "supervisor",
        verify_routing,
        {
            "synthesizer": "synthesizer",
            "end": END
        }
    )
    
    return workflow.compile()

def perform_research(query: str) -> dict:
    app = build_graph()
    initial_state = {
        "query": query,
        "expanded_queries": [],
        "retrieved_docs": [],
        "critique_log": "",
        "draft": "",
        "verification_errors": [],
        "revision_count": 0,
        "logs": [f"System: Orchestration Engine started. Research topic: '{query}'"]
    }
    
    print(f"Executing LangGraph for query: {query}")
    final_state = app.invoke(initial_state)
    
    return {
        "query": final_state["query"],
        "draft": final_state["draft"],
        "logs": final_state["logs"]
    }
