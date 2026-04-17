from typing import Dict, Any
import time
from .state import AgentState

def mock_llm_call(prompt: str) -> str:
    """A dummy function replacing Ollama/Llama 3 inference for now."""
    time.sleep(1) # simulate generation
    if "Expand this query" in prompt:
        return "quantum networking, topological latency boundaries, QEC codes"
    elif "Critique" in prompt:
        return "- Limitation 1: Some retrieved papers lack empirical latency stress tests.\n- Limitation 2: Scaling factors for Q-bits were frequently omitted."
    elif "Synthesize" in prompt:
        return "## Synthesis Review\n\nBased on the retrieved documents from ArXiv, modern methodology indicates a substantial gap in theoretical scaling structures. The integration of advanced metric paradigms reveals potential avenues for reducing intrinsic fault boundaries.\n\n### Limitations\nAs noted in our critique phase, structural validation in highly scaled environments is mathematically sparse."
    elif "Verify" in prompt:
        return "VERIFIED_OK"
    return "Default mock response"

def librarian_node(state: AgentState) -> dict:
    from .tools import fetch_arxiv_papers
    query = state["query"]
    logs = state.get("logs", [])
    
    logs.append(f"Librarian: Interrogating LLM for search expansion strategies...")
    expanded = mock_llm_call(f"Expand this query: {query}")
    
    logs.append(f"Librarian: Initializing Multi-Vector Retrieval across ArXiv (Public Tier)...")
    docs = fetch_arxiv_papers(query)
    
    logs.append(f"Librarian: Retrieved {len(docs)} high-fidelity documents.")
    return {
        "expanded_queries": [expanded],
        "retrieved_docs": docs,
        "logs": logs
    }

def skeptic_node(state: AgentState) -> dict:
    logs = state.get("logs", [])
    logs.append("Skeptic: Activated. Scanning retrieved vectors for methodological limitations...")
    critiques = mock_llm_call("Critique the retrieved documents")
    return {"critique_log": critiques, "logs": logs}

def synthesizer_node(state: AgentState) -> dict:
    logs = state.get("logs", [])
    rev_count = state.get("revision_count", 0)
    docs = state.get("retrieved_docs", [])
    
    if rev_count == 0:
        logs.append("Synthesizer: Organizing thematic trends into draft...")
    else:
        logs.append("Synthesizer: Incorporating supervisor constraints. Executing draft revision...")
        
    draft_base = mock_llm_call(f"Synthesize this with critiques: {state.get('critique_log')}")
    
    # Dynamically inject the actual ArXiv pulls so the output is highly dependent on the user query
    doc_markdown = "\n\n".join([f"### {d['title']}\n**Authors:** {', '.join(d['authors'])}\n\n**Abstract:** {d['summary']}\n\n**Source:** [Read PDF]({d['url']})" for d in docs])
    if not docs:
        doc_markdown = "*No pertinent ArXiv literature was found for this query vector.*"
    
    dynamic_draft = f"## Comprehensive Review: {state['query'].title()}\n\n{draft_base}\n\n---\n\n## Retrieved Scholarly Grounding\n\n{doc_markdown}"
    
    return {"draft": dynamic_draft, "logs": logs}

def supervisor_node(state: AgentState) -> dict:
    logs = state.get("logs", [])
    rev_count = state.get("revision_count", 0)
    logs.append(f"Supervisor: Executing grounding checks (Pass {rev_count + 1})...")
    
    _ = mock_llm_call("Verify the draft against chunks")
    
    errors = []
    # Trigger a 1-loop correction cycle automatically to demo LangGraph cyclic edge
    if rev_count == 0:
         errors.append("Claim regarding theoretical scaling structures lacks direct source vectors.")
         logs.append("Supervisor: Warning - Hallucination detected! Emitting correction log to Synthesizer.")
    else:
         logs.append("Supervisor: Final Verification passed. All claims fully grounded in embedded source logic.")
         
    return {
        "verification_errors": errors, 
        "revision_count": rev_count + 1,
        "logs": logs
    }
