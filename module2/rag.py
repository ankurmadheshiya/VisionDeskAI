import os
import google.generativeai as genai
from module2.embeddings import EmbeddingGenerator
from module2.vector_db import ChromaDBManager

class RAGPipeline:
    """
    Implements a Retrieval-Augmented Generation (RAG) pipeline.

    This class coordinates the flow of:
    1. Embedding a user question.
    2. Searching ChromaDB to find the most relevant document chunks.
    3. Building a structured prompt combining the retrieved context and question.
    4. Submitting the prompt to the Gemini API (if GEMINI_API_KEY is configured)
       or utilizing a fallback local summarization engine if no key is present.
    """

    def __init__(self, db_path: str = None, embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the pipeline with embeddings and vector database managers.

        Args:
            db_path (str, optional): Path to the ChromaDB storage folder.
            embedding_model_name (str): Model name for SentenceTransformers.
        """
        # Instantiate the embedding generator to embed query strings
        self.embedding_gen = EmbeddingGenerator(model_name=embedding_model_name)
        
        # Instantiate the ChromaDB manager to handle collection search
        self.db_manager = ChromaDBManager(db_path=db_path)

        # Check if Gemini API key is configured in environmental variables
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            # Configure the google-generativeai client with the API key
            genai.configure(api_key=self.api_key)
            self.has_gemini = True
        else:
            self.has_gemini = False

    def query_rag(self, collection_name: str, query: str, n_results: int = 3) -> dict:
        """
        Processes a user question end-to-end through the RAG pipeline.

        Args:
            collection_name (str): The name of the document collection in ChromaDB.
            query (str): The user's question.
            n_results (int): The number of context chunks to retrieve (default is 3).

        Returns:
            dict: A dictionary containing:
                - "answer" (str): The generated answer.
                - "retrieved_chunks" (list[dict]): The raw chunks used as context.
                - "engine" (str): The response engine used ('Gemini' or 'Local Heuristic Summary').
        """
        # Step 1: Generate an embedding representation for the user query
        query_embedding = self.embedding_gen.generate_single_embedding(query)

        # Step 2: Query ChromaDB for the closest matching document chunks
        matched_chunks = self.db_manager.query_similarity(
            collection_name=collection_name,
            query_embedding=query_embedding,
            n_results=n_results
        )

        # Handle case where no documents have been uploaded/stored
        if not matched_chunks:
            return {
                "answer": "No documents found in the database. Please upload a PDF first.",
                "retrieved_chunks": [],
                "engine": "System"
            }

        # Step 3: Extract text blocks and build context string for the prompt
        context_parts = []
        for chunk in matched_chunks:
            page_num = chunk["metadata"].get("page_number", "Unknown") if chunk["metadata"] else "Unknown"
            context_parts.append(f"[Page {page_num}]: {chunk['text']}")
        
        context_str = "\n\n".join(context_parts)

        # Step 4: Generate the response based on availability of Gemini API Key
        if self.has_gemini:
            # Construct the system prompt instructing the LLM to ground its answer in the context
            prompt = (
                "You are an expert AI assistant. Answer the user's question using ONLY the provided context blocks "
                "extracted from a document.\n"
                "If the context does not contain enough information to answer the question, state that clearly.\n"
                "Always reference the page numbers of the context blocks you used to construct your answer.\n\n"
                f"Context:\n{context_str}\n\n"
                f"Question: {query}\n"
                "Answer:"
            )

            try:
                # Load the Gemini model
                model = genai.GenerativeModel("gemini-1.5-flash")
                # Generate answer
                response = model.generate_content(prompt)
                answer = response.text.strip()
                engine = "Gemini"
            except Exception as e:
                # Fall back to heuristic engine in case Gemini API fails during runtime (quota, internet, etc.)
                answer = (
                    f"[Gemini API Call Failed: {str(e)}]\n\n"
                    "Local Summary Fallback:\n" + self._generate_heuristic_answer(query, matched_chunks)
                )
                engine = "Local Heuristic Summary (Fallback)"
        else:
            # Generate a structured answer locally without calling external APIs
            answer = (
                "[WARNING] GEMINI_API_KEY environment variable is not set. Showing local semantic synthesis.\n"
                "To enable real generative answers, set the GEMINI_API_KEY environment variable.\n\n"
                + self._generate_heuristic_answer(query, matched_chunks)
            )
            engine = "Local Heuristic Summary"

        return {
            "answer": answer,
            "retrieved_chunks": matched_chunks,
            "engine": engine
        }

    def _generate_heuristic_answer(self, query: str, matched_chunks: list[dict]) -> str:
        """
        Generates a summary/answer locally using heuristic keyword matching of chunks.

        This acts as a robust backup to guarantee the app compiles, runs, and demonstrates
        correct similarity search and document reference tracking even when no internet connection
        or Gemini credentials are available.

        Args:
            query (str): The original question.
            matched_chunks (list[dict]): Retrieved document chunks.

        Returns:
            str: A formatted text block summarizing semantic matches and page references.
        """
        # Break down the user question into keywords
        keywords = set(query.lower().split())
        # Remove common short stopwords
        stopwords = {"what", "is", "the", "a", "an", "of", "and", "in", "to", "for", "on", "with", "how", "why", "are", "you"}
        meaningful_keywords = keywords - stopwords

        synthesis_lines = ["Here are the most relevant sections found in the document:"]

        # Loop through chunks and pull the most matching sentences
        for idx, chunk in enumerate(matched_chunks):
            page_num = chunk["metadata"].get("page_number", "Unknown") if chunk["metadata"] else "Unknown"
            text = chunk["text"]
            
            # Split paragraph into sentences
            sentences = text.split(". ")
            best_sentences = []
            
            # Find sentences containing query keywords
            for sentence in sentences:
                sentence_lower = sentence.lower()
                # If any key term matches, select the sentence
                if any(keyword in sentence_lower for keyword in meaningful_keywords):
                    best_sentences.append(sentence.strip())
            
            # Format the output for this page reference
            if best_sentences:
                selected_text = ". ".join(best_sentences[:3]) # Limit to top 3 matching sentences
            else:
                # If no direct keyword matches, show a snippet of the beginning of the chunk
                selected_text = " ".join(text.split()[:30]) + "..."

            synthesis_lines.append(f"- [From Page {page_num}]: \"{selected_text}\"")

        synthesis_lines.append("\nGrounding Context Source Information:")
        for idx, chunk in enumerate(matched_chunks):
            page_num = chunk["metadata"].get("page_number", "Unknown") if chunk["metadata"] else "Unknown"
            synthesis_lines.append(f"  - Source Chunk {idx+1} (Page {page_num}, Similarity Distance Score: {chunk['distance']:.4f})")

        return "\n".join(synthesis_lines)
