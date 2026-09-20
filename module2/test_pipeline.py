import os
import fitz  # PyMuPDF
from module2.pdf_parser import extract_text_from_pdf
from module2.chunking import split_text_into_chunks
from module2.embeddings import EmbeddingGenerator
from module2.vector_db import ChromaDBManager
from module2.rag import RAGPipeline

def create_sample_pdf(file_path: str):
    """
    Creates a sample multi-page PDF document programmatically using PyMuPDF.

    This ensures that we have a standard test document with predictable text
    content across multiple pages, making verification reproducible.

    Args:
        file_path (str): The file path where the generated PDF will be saved.
    """
    print(f"Creating sample test PDF at: {file_path}")
    
    # Initialize a new empty PDF document
    doc = fitz.open()
    
    # Page 1 content: VisionDeskAI Overview
    page1 = doc.new_page()
    page1_text = (
        "VisionDeskAI Overview and System Architecture\n\n"
        "VisionDeskAI is an advanced web application designed for intelligent desktop surveillance "
        "and document processing. Module 1 deals with video object detection using the YOLO algorithm. "
        "It processes webcam feeds and triggers alerts when people or forbidden objects are detected. "
        "Module 2 is the RAG (Retrieval-Augmented Generation) document intelligence system. It allows users "
        "to upload PDF documentation, extracts text automatically, processes it into semantic vector databases "
        "using ChromaDB and sentence-transformers, and answers natural language questions."
    )
    # Insert text on page 1 at position (x=50, y=50)
    page1.insert_text((50, 50), page1_text)
    
    # Page 2 content: RAG Pipeline Details
    page2 = doc.new_page()
    page2_text = (
        "Retrieval-Augmented Generation (RAG) Specifications\n\n"
        "The RAG system in Module 2 follows a five-step lifecycle:\n"
        "1. Extraction: High-fidelity text extraction using PyMuPDF (fitz).\n"
        "2. Chunking: Text is segmented into 200-word chunks with a 40-word overlap.\n"
        "3. Embedding: The sentence-transformers model 'all-MiniLM-L6-v2' maps chunks to 384-dimensional vectors.\n"
        "4. Storage: Vectors and page metadata are stored in a persistent ChromaDB database on disk.\n"
        "5. Retrieval & Generation: Questions are vectorized, similar chunks are retrieved, and a grounded answer is "
        "synthesized using either the Google Gemini API or a local summary fallback when API keys are not provided."
    )
    # Insert text on page 2 at position (x=50, y=50)
    page2.insert_text((50, 50), page2_text)

    # Save the document and release resources
    doc.save(file_path)
    doc.close()
    print("Sample PDF created successfully.")


def run_test_pipeline():
    """
    Executes the entire end-to-end RAG pipeline locally to verify correctness.
    """
    print("\n--- Starting End-to-End RAG Pipeline Test ---\n")
    
    # Define file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_pdf_path = os.path.join(current_dir, "sample_test.pdf")
    test_db_path = os.path.join(current_dir, "test_chroma_db")
    collection_name = "test_collection"

    # Step 1: Create a test PDF
    create_sample_pdf(sample_pdf_path)

    # Step 2: Test PDF Parser
    print("\nStep 2: Parsing PDF document...")
    parsed_pages = extract_text_from_pdf(sample_pdf_path)
    for page in parsed_pages:
        print(f"  - Extracted page {page['page_number']} ({len(page['text'].split())} words)")

    # Step 3: Test Text Chunking
    print("\nStep 3: Chunking text...")
    chunks = split_text_into_chunks(parsed_pages, chunk_size=100, chunk_overlap=20)
    print(f"  - Generated {len(chunks)} chunks.")
    for chunk in chunks:
         print(f"    - Chunk {chunk['chunk_index']} (Page {chunk['metadata']['page_number']}): \"{chunk['text'][:60]}...\"")

    # Step 4: Test Embeddings Generation
    print("\nStep 4: Generating embeddings...")
    embedding_gen = EmbeddingGenerator()
    texts_to_embed = [c["text"] for c in chunks]
    embeddings = embedding_gen.generate_embeddings(texts_to_embed)
    print(f"  - Successfully generated {len(embeddings)} embeddings vectors.")
    print(f"  - Embedding vector dimension: {len(embeddings[0])} dimensions.")

    # Step 5: Test ChromaDB Storage
    print("\nStep 5: Storing inside ChromaDB...")
    db_manager = ChromaDBManager(db_path=test_db_path)
    
    # Reset/clear previous collection if exists
    db_manager.delete_collection(collection_name)
    
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [c["metadata"] for c in chunks]
    
    db_manager.add_documents(
        collection_name=collection_name,
        documents=texts_to_embed,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"  - Stored {len(texts_to_embed)} items in collection '{collection_name}'.")

    # Step 6: Test RAG Query
    print("\nStep 6: Running RAG pipeline query...")
    # Initialize RAG Pipeline pointing to the test DB
    pipeline = RAGPipeline(db_path=test_db_path)
    
    # Test query 1: Ask about system overview
    question = "What is VisionDeskAI and what does Module 1 do?"
    print(f"\nQuestion: {question}")
    result = pipeline.query_rag(collection_name=collection_name, query=question, n_results=2)
    print(f"Engine: {result['engine']}")
    print(f"Answer:\n{result['answer']}")

    # Clean up test files to avoid leaving clutter
    print("\nCleaning up test files...")
    if os.path.exists(sample_pdf_path):
        os.remove(sample_pdf_path)
    
    # Clean up the test database collection
    db_manager.delete_collection(collection_name)
    print("Cleanup complete.")
    print("\n--- Pipeline Test Finished Successfully! ---")


if __name__ == "__main__":
    run_test_pipeline()
