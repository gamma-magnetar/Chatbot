# 📊 PPT-PDF RAG Chatbot (Multimodal)

A **Retrieval-Augmented Generation (RAG) chatbot** that answers questions from **PPT-based PDFs**, including **image-heavy slides and charts**, using **text extraction, OCR, and vision-based LLMs**.  
The system is deployed using **Streamlit** and produces **grounded, hallucination-safe answers**.

---

## 🚀 Features

- Supports **text-based PDFs** and **image-heavy PPT PDFs**
- **Vision-based chart & slide understanding**
- OCR fallback for embedded images
- FAISS-based vector search
- Hallucination-safe RAG pipeline
- Interactive Streamlit UI

---

## 🧠 Models Used

### Embedding Model
- **sentence-transformers/all-MiniLM-L6-v2**
- Converts document chunks into dense vector embeddings
- Chosen for speed and semantic retrieval quality

### Language Model (Answer Generation)
- **OpenAI GPT-4o / GPT-4o-mini**
- Generates answers strictly from retrieved context

### Vision Model (Charts & Images)
- **GPT-4o (Vision)**
- Interprets charts, trends, and visual relationships
- Converts visual content into textual summaries for RAG

---

## 🏗️ Architecture

PDF Upload
↓
Text Extraction (pdfplumber)
↓
Image OCR (Tesseract)
↓
Vision-based Slide Understanding (GPT-4o Vision)
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


---

## 📁 Project Structure



ppt-pdf-rag-chatbot/
│
├── app.py # Streamlit UI & session handling
├── ingest.py # PDF ingestion & vector index creation
├── rag.py # Retrieval + answer generation
├── ocr_utils.py # OCR utilities for images
├── vision_utils.py # Vision-based chart & slide understanding
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/ # Runtime data (ignored in Git)


---

## ⚙️ How It Works

1. **PDF Ingestion**
   - Extracts selectable text from PDF
   - Extracts embedded images and applies OCR

2. **Vision Processing (Image-Heavy PDFs)**
   - Converts each slide/page into an image
   - Vision LLM describes charts, trends, and insights

3. **Chunking & Embeddings**
   - All extracted content is chunked
   - Chunks converted into vector embeddings

4. **Retrieval-Augmented Generation**
   - Relevant chunks retrieved using FAISS
   - LLM answers strictly from retrieved context

---

## 🖥️ Running Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2️⃣ Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set API key
# Windows (PowerShell)
setx OPENAI_API_KEY "your_api_key_here"

# macOS/Linux
export OPENAI_API_KEY="your_api_key_here"


Restart the terminal after setting the key.

5️⃣ Run the app
streamlit run app.py


Open:

http://localhost:8501

🧪 Usage

Upload a PPT-based PDF

Wait for ingestion to complete

Ask questions such as:

“What trend does the revenue chart show?”

“Summarize the key insights from the slides”

“What conclusion is drawn in the presentation?”

If no usable content is found, the app safely disables querying.

⚠️ Notes

Vision-based ingestion requires sufficient API quota

Vision processing is triggered only for image-heavy PDFs

Text-only PDFs continue to work without vision calls

🔮 Future Improvements

Slide-level citations in answers

Vision output caching to reduce cost

Hybrid search (BM25 + vector)

Multi-document knowledge base

📌 Summary

This project demonstrates a production-style multimodal RAG system capable of understanding text, charts, and visuals inside PPT-based PDFs, combining:

Document intelligence

Vision-based LLMs

Vector search

Streamlit deployment
