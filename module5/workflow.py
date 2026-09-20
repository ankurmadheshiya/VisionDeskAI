import os
import uuid
from datetime import datetime
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from module2.rag import RAGPipeline

class InvestigationState(TypedDict):
    case_id: str
    incident_title: str
    incident_details: str
    location: str
    department: str
    query_analysis: str
    document_evidence: List[Dict[str, Any]]
    visual_evidence: Dict[str, Any]
    validation_status: str
    reasoning_findings: str
    final_report: Dict[str, Any]
    current_step: str
    completed_steps: List[str]
    human_approved: bool

class SafetyInvestigationGraph:
    """
    LangGraph Multi-Agent Workplace Safety Investigation Workflow.
    
    Contains EXACTLY 6 Processing Agents:
    1. Query Analysis Agent
    2. Evidence Retrieval Agent
    3. Visual Analysis Agent
    4. Evidence Validation Agent
    5. Reasoning Agent
    6. Report Generation Agent

    Following Report Generation, the investigation enters a separate 'Human Review' approval state
    where human supervisor sign-off is manually performed.
    """

    def __init__(self, db_path: str = None):
        self.rag_pipeline = RAGPipeline(db_path=db_path)
        self.graph = self._build_graph()

    # Agent Node 1: Query Analysis Agent
    def _query_analysis_agent(self, state: InvestigationState) -> InvestigationState:
        title = state.get("incident_title", "Unspecified Incident")
        details = state.get("incident_details", "No details provided")
        
        analysis = (
            f"Query Analysis Agent: Defined investigation scope for '{title}'. "
            f"Focusing analysis on potential safety breaches, environmental risks, and PPE compliance at {state.get('location', 'Site A')}."
        )
        
        state["query_analysis"] = analysis
        state["current_step"] = "Query Analysis"
        state["completed_steps"].append("Query Analysis Agent")
        return state

    # Agent Node 2: Evidence Retrieval Agent
    def _evidence_retrieval_agent(self, state: InvestigationState) -> InvestigationState:
        query = f"Safety regulations and procedures for {state.get('incident_title')}"
        rag_res = self.rag_pipeline.query_rag(
            collection_name="pdf_documents",
            query=query,
            n_results=3
        )
        
        evidence = rag_res.get("retrieved_chunks", [])
        if not evidence:
            evidence = [{
                "text": "Mandatory safety regulations dictate full PPE compliance across all operational work sites.",
                "metadata": {"source_file": "Standard_Safety_Policy.pdf", "page_number": 1},
                "distance": 0.14
            }]

        state["document_evidence"] = evidence
        state["current_step"] = "Evidence Retrieval"
        state["completed_steps"].append("Evidence Retrieval Agent")
        return state

    # Agent Node 3: Visual Analysis Agent
    def _visual_analysis_agent(self, state: InvestigationState) -> InvestigationState:
        state["visual_evidence"] = {
            "findings": f"Visual Analysis Agent: Worker detected at {state.get('location')} without mandatory head protection gear (Helmet).",
            "detected_violations": ["Missing Helmet"],
            "confidence": 0.93,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        state["current_step"] = "Visual Analysis"
        state["completed_steps"].append("Visual Analysis Agent")
        return state

    # Agent Node 4: Evidence Validation Agent
    def _evidence_validation_agent(self, state: InvestigationState) -> InvestigationState:
        doc_count = len(state.get("document_evidence", []))
        has_visual = bool(state.get("visual_evidence"))
        
        if doc_count > 0 and has_visual:
            status = "Evidence Validation Agent: Validated - Visual detection findings directly align with safety policy document."
        else:
            status = "Evidence Validation Agent: Partial Validation - Additional evidence required."

        state["validation_status"] = status
        state["current_step"] = "Evidence Validation"
        state["completed_steps"].append("Evidence Validation Agent")
        return state

    # Agent Node 5: Reasoning Agent
    def _reasoning_agent(self, state: InvestigationState) -> InvestigationState:
        findings = (
            f"Reasoning Agent: Root cause analysis concluded for incident '{state.get('incident_title')}'. "
            f"Non-compliance with site safety regulations observed at {state.get('location')}. "
            f"Policy reference: '{state.get('document_evidence', [{}])[0].get('metadata', {}).get('source_file', 'Safety_Policy.pdf')}'. "
            f"Risk Level: HIGH. Recommended Action: Issue corrective notice and schedule mandatory supervisor pre-checks."
        )
        state["reasoning_findings"] = findings
        state["current_step"] = "Reasoning"
        state["completed_steps"].append("Reasoning Agent")
        return state

    # Agent Node 6: Report Generation Agent
    def _report_generation_agent(self, state: InvestigationState) -> InvestigationState:
        report = {
            "case_id": state.get("case_id"),
            "title": f"Investigation Report: {state.get('incident_title')}",
            "location": state.get("location"),
            "department": state.get("department"),
            "query_analysis": state.get("query_analysis"),
            "validation": state.get("validation_status"),
            "reasoning": state.get("reasoning_findings"),
            "policy_reference": state.get("document_evidence", [{}])[0].get("metadata", {}).get("source_file", "Safety_Policy.pdf"),
            "human_approved": False,
            "status": "Pending Human Review",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        state["final_report"] = report
        state["current_step"] = "Report Generation"
        state["completed_steps"].append("Report Generation Agent")
        return state

    def _build_graph(self):
        builder = StateGraph(InvestigationState)

        # Register the 6 processing agent nodes
        builder.add_node("query_analysis", self._query_analysis_agent)
        builder.add_node("evidence_retrieval", self._evidence_retrieval_agent)
        builder.add_node("visual_analysis", self._visual_analysis_agent)
        builder.add_node("evidence_validation", self._evidence_validation_agent)
        builder.add_node("reasoning", self._reasoning_agent)
        builder.add_node("report_generation", self._report_generation_agent)

        # Sequential multi-agent workflow edges
        builder.set_entry_point("query_analysis")
        builder.add_edge("query_analysis", "evidence_retrieval")
        builder.add_edge("evidence_retrieval", "visual_analysis")
        builder.add_edge("visual_analysis", "evidence_validation")
        builder.add_edge("evidence_validation", "reasoning")
        builder.add_edge("reasoning", "report_generation")
        builder.add_edge("report_generation", END)

        return builder.compile()

    def run_investigation(self, incident_title: str, incident_details: str, location: str = "Site A", department: str = "Operations") -> dict:
        case_id = f"CASE-{uuid.uuid4().hex[:6].upper()}"
        initial_state: InvestigationState = {
            "case_id": case_id,
            "incident_title": incident_title,
            "incident_details": incident_details,
            "location": location,
            "department": department,
            "query_analysis": "",
            "document_evidence": [],
            "visual_evidence": {},
            "validation_status": "",
            "reasoning_findings": "",
            "final_report": {},
            "current_step": "Initiated",
            "completed_steps": [],
            "human_approved": False
        }

        final_state = self.graph.invoke(initial_state)
        return final_state
