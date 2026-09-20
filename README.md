# VisionDesk AI – Multimodal Workplace Intelligence

An enterprise-grade Workplace Safety Intelligence platform combining **Computer Vision (YOLOv8 & OpenCV)**, **Document RAG (PyMuPDF & ChromaDB)**, **Multimodal Intelligence**, **Agentic AI Workflows (LangGraph)**, and **Interactive Safety Analytics & Reporting**.

---

## 🌟 Key Features & Module Overview

1. **Module 1 – Visual Data Processing & Safety Detection**
   - YOLOv8 + OpenCV visual inference for images and video feeds.
   - Detects workers and Personal Protective Equipment (PPE): **Helmet, Vest, Gloves, Mask, Shoes/Boots**.
   - Identifies safety violations, overlays bounding boxes, calculates confidence scores, timestamping, and logs findings to the database.

2. **Module 2 – Document Processing & Knowledge Extraction**
   - PyMuPDF text extraction from safety manuals, PDFs, and compliance documents.
   - Overlapping text chunking preserving page-level metadata.
   - `SentenceTransformers` (`all-MiniLM-L6-v2`, 384-dimensional dense vectors) and persistent vector storage in **ChromaDB**.

3. **Module 3 – Multimodal Intelligence Engine**
   - Fuses visual detection results (e.g., *Missing Helmet*) with retrieved document safety regulations from ChromaDB.
   - Synthesizes evidence-backed compliance insights with page references and policy citations.

4. **Module 4 – RAG & Grounded Question Answering**
   - Source-grounded QA pipeline preventing AI hallucination.
   - Displays retrieved context chunks, page numbers, similarity scores, and synthesized answers.

5. **Module 5 – Agentic Workflow (LangGraph)**
   - 6-Agent state graph workflow:
     1. `Query Analysis Agent`
     2. `Evidence Retrieval Agent`
     3. `Visual Analysis Agent`
     4. `Evidence Validation Agent`
     5. `Reasoning Agent`
     6. `Report Generation Agent`
   - **Human Review**: Requires manual supervisor sign-off before case closure.

6. **Module 6 – Enterprise Safety Dashboard & Reporting**
   - Sleek enterprise Streamlit dashboard with custom CSS, dark slate/emerald theme, top KPI cards, interactive Plotly charts, compliance matrix, and risk heatmaps.
   - Automated report exporter generating **CSV, Excel (`openpyxl`), and PDF (`reportlab`)** safety audit reports.

---

## 🛠️ Technology Stack

- **Frontend / Dashboard**: Streamlit, Custom HTML/CSS
- **Backend Framework**: Python 3.12+, FastAPI, Uvicorn, SQLAlchemy
- **Computer Vision**: YOLOv8 (Ultralytics), OpenCV
- **Document RAG & Embeddings**: PyMuPDF (`fitz`), SentenceTransformers (`all-MiniLM-L6-v2`), ChromaDB
- **Agentic AI**: LangGraph, LangChain
- **Reporting**: OpenPyXL (Excel), ReportLab (PDF), CSV
- **Database**: SQLite (default: `visiondesk.db`) / PostgreSQL compatible

---

## 🚀 How to Run the Application

### 1. Environment Setup
Activate the virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Start the Unified FastAPI Backend
```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000
```
- API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 3. Launch the Streamlit Enterprise Dashboard
```powershell
.\.venv\Scripts\streamlit.exe run streamlit_app.py
```
- Open browser at: [http://localhost:8501](http://localhost:8501)

---

## 🔑 Environment Variables

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./visiondesk.db
API_BASE_URL=http://127.0.0.1:8000
```

---

## 📡 REST API Endpoints Summary

- `GET /health` - API & Database health status
- `POST /signup` & `POST /login` - User authentication
- `POST /detect/image` - OpenCV + YOLOv8 PPE image detection
- `POST /upload` - PDF document ingestion into ChromaDB
- `POST /query` - RAG semantic vector search & Q&A
- `POST /multimodal-insight` - Visual + RAG document fusion
- `POST /investigate` - Trigger LangGraph multi-agent workflow
- `POST /investigate/approve` - Human supervisor sign-off
- `GET /violations` & `GET /stats` - Safety analytics & violation logs
- `POST /export/report` - Export safety report (CSV, Excel, PDF)
