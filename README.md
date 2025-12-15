PPT-PDF RAG Chatbot (Text + Vision)
Overview

This project implements a Retrieval-Augmented Generation (RAG) chatbot that can answer questions from PPT-based PDFs, including image-heavy slides and charts.

The system supports:

✅ Text-based PDFs (reports, documents)

✅ Image-heavy PPT PDFs (slides, charts, diagrams)

✅ Vision-based understanding of charts and visuals

✅ Grounded answers (no hallucinations)

It combines PDF parsing, OCR, vision-LLMs, vector search (FAISS), and LLMs into a single Streamlit application.

🧠 High-Level Architecture
4
Pipeline Flow
PDF Upload
   ↓
Text Extraction (pdfplumber)
   ↓
Image OCR (Tesseract)
   ↓
Vision-based Slide Understanding (GPT-4o / Vision LLM)
   ↓
Chunking
   ↓
Embeddings (Sentence Transformers)
   ↓
FAISS Vector Store
   ↓
User Query
   ↓
Context Retrieval
   ↓
LLM Answer (Grounded Response)

✨ Key Features

Multimodal RAG

Handles both text and image-only PPT PDFs

Chart & Slide Understanding

Vision LLM explains charts, trends, comparisons

Hallucination-Safe

Answers only from retrieved document context

Modular & Extensible

OCR, vision, embeddings, and retrieval are cleanly separated

Interactive UI

Streamlit-based web interface

🧠 Models Used
1️⃣ Embedding Model

Model: sentence-transformers/all-MiniLM-L6-v2

Purpose: Convert document chunks into vector embeddings

Why: Fast, lightweight, high-quality semantic search

2️⃣ Language Model (Text)

Model: OpenAI GPT-4o / GPT-4o-mini

Purpose: Generate final answers from retrieved context

Behavior: Strictly grounded in retrieved chunks

3️⃣ Vision Model (Charts & Images)

Model: GPT-4o (Vision)

Purpose:

Understand charts visually

Explain trends, comparisons, and insights

Convert visual information into text for RAG

Why Vision is required:

OCR alone cannot understand chart relationships or trends

📁 Project Structure
ppt-pdf-rag-chatbot/
│
├── app.py                # Streamlit UI & session management
├── ingest.py             # PDF ingestion & vector index creation
├── rag.py                # Retrieval + LLM answering logic
├── ocr_utils.py          # Image OCR utilities
├── vision_utils.py       # Vision-based slide & chart understanding
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/                 # (Ignored) Runtime data, FAISS index, uploads

⚙️ How It Works (Detailed)
Step 1: PDF Ingestion

Extracts selectable text using pdfplumber

Extracts embedded images and applies OCR

Detects image-heavy PDFs

Step 2: Vision-Based Understanding (Image-Heavy PDFs)

Converts each slide/page into an image

Sends image to a vision-capable LLM

Generates a textual explanation of charts and visuals

Step 3: Chunking & Embeddings

All extracted text (text + OCR + vision summaries) is chunked

Each chunk is embedded using Sentence Transformers

Step 4: Vector Storage

Embeddings stored in FAISS

Enables fast semantic retrieval

Step 5: Question Answering (RAG)

User query is embedded

Top-k relevant chunks retrieved

LLM answers using only retrieved context

🖥️ Running the App Locally
1️⃣ Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2️⃣ Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set API Key
# Windows (PowerShell)
setx OPENAI_API_KEY "your_api_key_here"

# Mac/Linux
export OPENAI_API_KEY="your_api_key_here"


Restart the terminal after setting the key.

5️⃣ Run Streamlit
streamlit run app.py


Open in browser:

http://localhost:8501

🚦 Usage Instructions

Upload a PDF (including PPT-based PDFs)

Wait for ingestion to complete

Ask questions like:

“What trend does the revenue chart show?”

“Summarize the key insights from this presentation”

“What conclusion is drawn in the final slides?”

If the document contains no usable content, the app safely disables querying.

⚠️ Notes on API Usage

Vision models require sufficient API quota

If quota is exhausted:

Text-based PDFs still work

Vision ingestion may fail gracefully

Vision extraction is triggered only for image-heavy PDFs to reduce cost

🔮 Future Improvements

Slide-level citations in answers

Caching vision summaries to reduce cost

Toggle between OCR-only and Vision-mode

Hybrid search (BM25 + vector)

Multi-PDF knowledge base

📌 Summary

This project demonstrates a production-style multimodal RAG system capable of understanding text, images, and charts inside PPT-based PDFs, combining:

Document intelligence

Vision-LLMs

Vector databases

Streamlit deployment
