# Chatbot
# PPT-PDF RAG Chatbot

## Overview
A Retrieval-Augmented Generation chatbot that ingests PPT-based PDFs,
extracts both textual and chart-based information using OCR, stores embeddings
in a FAISS vector database, and answers user queries grounded strictly in the
document content.

## Architecture
PDF Upload → Text & Chart Extraction → Chunking → Embeddings → FAISS →
LLM-based Answering

## Features
- Handles PPT-style PDFs
- OCR-based chart and image understanding
- Prevents hallucinations using RAG
- Deployed using Streamlit Cloud

## Tech Stack
- Python, Streamlit
- FAISS, Sentence Transformers
- PyMuPDF, Tesseract OCR
- OpenAI GPT

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
