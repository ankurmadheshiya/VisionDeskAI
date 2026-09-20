import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from pydantic import BaseModel

# Import our custom RAG modules
from module2.pdf_parser import extract_text_from_pdf
from module2.chunking import split_text_into_chunks
from module2.embeddings import EmbeddingGenerator
from module2.vector_db import ChromaDBManager
from module2.rag import RAGPipeline

# Initialize the self-contained FastAPI application
app = FastAPI(
    title="VisionDeskAI RAG API (Module 2)",
    description="College project API for PDF parsing, text chunking, embedding generation, ChromaDB vector storage, and RAG query processing.",
    version="1.0.0"
)

# Define directories relative to this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(CURRENT_DIR, "uploads")
DB_DIR = os.path.join(CURRENT_DIR, "chroma_db")

# Ensure necessary directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize pipeline managers
embedding_generator = EmbeddingGenerator()
db_manager = ChromaDBManager(db_path=DB_DIR)
rag_pipeline = RAGPipeline(db_path=DB_DIR)

# Define schemas for API requests
class QueryRequest(BaseModel):
    query: str
    collection_name: str = "pdf_documents"
    n_results: int = 3

@app.get("/health")
def health_check():
    """
    Endpoint to check the health status of the API.

    Returns configuration details such as database directory existence
    and whether the Gemini API integration is active.
    """
    return {
        "status": "healthy",
        "module": "Module 2 (RAG)",
        "db_directory": DB_DIR,
        "uploads_directory": UPLOAD_DIR,
        "gemini_api_key_configured": os.environ.get("GEMINI_API_KEY") is not None
    }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    collection_name: str = Query("pdf_documents", description="The ChromaDB collection to store the embeddings in.")
):
    """
    Endpoint to upload a PDF file and process it through the pipeline:
    1. Saves the PDF file to disk in the uploads directory.
    2. Extracts text from the PDF using PyMuPDF.
    3. Splits text into semantic chunks with overlap.
    4. Generates dense vector embeddings using sentence-transformers (all-MiniLM-L6-v2).
    5. Saves text, embeddings, and metadata into a persistent ChromaDB collection.

    Args:
        file (UploadFile): The PDF document to be uploaded.
        collection_name (str): The target ChromaDB collection (default: 'pdf_documents').

    Returns:
        dict: A summary of the upload process including number of chunks generated and stored.
    """
    # Verify that the uploaded file is a PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a PDF file."
        )

    # Clean the filename to prevent folder traversal and save it to the upload folder
    safe_filename = os.path.basename(file.filename)
    saved_file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        # Save file to uploads folder
        with open(saved_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file to disk. Error: {str(e)}"
        )

    # Execute the processing pipeline
    try:
        # Step 1: Parse the PDF pages and extract text
        pages_text = extract_text_from_pdf(saved_file_path)
        
        if not pages_text:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF contains no extractable text."
            )

        # Step 2: Split text into overlapping word chunks
        chunks = split_text_into_chunks(pages_text, chunk_size=200, chunk_overlap=40)

        # Step 3: Prepare arrays for ChromaDB ingestion
        documents_list = []
        embeddings_list = []
        metadatas_list = []
        ids_list = []

        # Iterate through chunks and compile documents and metadata
        for chunk in chunks:
            chunk_text = chunk["text"]
            page_num = chunk["metadata"]["page_number"]

            # Generate unique ID for each chunk
            chunk_id = f"{safe_filename}_p{page_num}_{uuid.uuid4().hex[:8]}"

            # Accumulate values
            documents_list.append(chunk_text)
            metadatas_list.append({
                "source_file": safe_filename,
                "page_number": page_num
            })
            ids_list.append(chunk_id)

        # Step 4: Generate vector embeddings for all chunks in a single batch
        embeddings_list = embedding_generator.generate_embeddings(documents_list)

        # Step 5: Store documents, embeddings, and metadata in ChromaDB
        db_manager.add_documents(
            collection_name=collection_name,
            documents=documents_list,
            embeddings=embeddings_list,
            metadatas=metadatas_list,
            ids=ids_list
        )

        return {
            "message": "PDF uploaded and indexed successfully.",
            "filename": safe_filename,
            "collection_name": collection_name,
            "total_pages": len(pages_text),
            "total_chunks_indexed": len(documents_list)
        }

    except Exception as e:
        # If any step fails, remove the saved file and raise an API error
        if os.path.exists(saved_file_path):
            os.remove(saved_file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF document. Error: {str(e)}"
        )

@app.post("/query")
def query_documents(request: QueryRequest):
    """
    Endpoint to ask questions based on uploaded documents.

    It queries ChromaDB using the question embedding, retrieves the most similar chunks,
    and returns a RAG response grounding the answer with page references.

    Args:
        request (QueryRequest): The query payload containing 'query', 'collection_name', and 'n_results'.

    Returns:
        dict: The synthesized answer, retrieved source text chunks, and the response engine metadata.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'query' cannot be empty."
        )

    try:
        # Run the RAG pipeline end-to-end (query embedding -> retrieval -> prompt/generation)
        result = rag_pipeline.query_rag(
            collection_name=request.collection_name,
            query=request.query,
            n_results=request.n_results
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process RAG query. Error: {str(e)}"
        )
