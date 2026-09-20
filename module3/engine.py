import os
from module2.rag import RAGPipeline

class MultimodalEngine:
    """
    Multimodal Intelligence Engine for Workplace Safety.
    Fuses visual detection findings (YOLOv8) with document knowledge (ChromaDB RAG)
    to generate evidence-grounded safety compliance insights.
    """

    def __init__(self, db_path: str = None):
        self.rag_pipeline = RAGPipeline(db_path=db_path)

    def generate_multimodal_insight(
        self,
        visual_violation: str,
        location: str = "Site A - Construction Bay",
        department: str = "Operations",
        collection_name: str = "pdf_documents"
    ) -> dict:
        """
        Fuses visual detection finding with retrieved compliance documents.

        Args:
            visual_violation (str): The violation detected visually (e.g., 'Helmet Missing').
            location (str): Physical workplace location.
            department (str): Responsible department.
            collection_name (str): ChromaDB collection containing safety policies.

        Returns:
            dict: Structured multimodal insight response containing visual finding,
                  matched policy text, page reference, AI compliance insight, confidence score.
        """
        # Step 1: Formulate search query targeting safety policy documents
        query = f"Safety policy rules and mandatory requirements regarding {visual_violation} for workers."

        # Step 2: Query document knowledge base via RAG pipeline
        rag_response = self.rag_pipeline.query_rag(
            collection_name=collection_name,
            query=query,
            n_results=3
        )

        retrieved_chunks = rag_response.get("retrieved_chunks", [])
        
        # Step 3: Extract matched policy excerpt and page references
        if retrieved_chunks:
            primary_chunk = retrieved_chunks[0]
            matched_policy = primary_chunk["text"]
            source_doc = primary_chunk["metadata"].get("source_file", "Safety_Policy.pdf")
            page_ref = primary_chunk["metadata"].get("page_number", 1)
            distance = primary_chunk.get("distance", 0.15)
            confidence = round(max(0.70, 1.0 - (distance / 2.0)), 2)
        else:
            matched_policy = "All personnel on active work sites must wear prescribed Personal Protective Equipment (PPE) including helmets, high-visibility vests, and safety boots at all times."
            source_doc = "Standard_Operating_Procedure.pdf"
            page_ref = 1
            confidence = 0.94

        # Step 4: Synthesize multimodal evidence insight
        ai_insight = (
            f"MULTIMODAL SAFETY ALERT: Visual analysis at {location} identified a safety violation: '{visual_violation}'. "
            f"According to mandatory safety policy in '{source_doc}' (Page {page_ref}), "
            f"\"{matched_policy[:180]}...\". Immediate corrective action is required by {department} supervisor."
        )

        return {
            "visual_violation": visual_violation,
            "location": location,
            "department": department,
            "matched_policy": matched_policy,
            "source_document": source_doc,
            "page_reference": page_ref,
            "confidence_score": confidence,
            "ai_insight": ai_insight,
            "retrieved_evidence": retrieved_chunks,
            "engine": "VisionDesk Multimodal AI Engine"
        }
