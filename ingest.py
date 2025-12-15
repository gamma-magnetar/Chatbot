import pdfplumber
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ocr_utils import extract_images_and_ocr

DATA_DIR = "data"
INDEX_DIR = "data/index"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def ingest_pdf(pdf_path):
    os.makedirs(INDEX_DIR, exist_ok=True)

    # 1. Extract text
    text = extract_text_from_pdf(pdf_path)

    # 2. Extract charts/images text
    ocr_text = extract_images_and_ocr(pdf_path)

    full_text = text + "\n" + ocr_text

    # 3. Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(full_text)

    # 4. Embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    # 5. FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    # 6. Persist index + chunks
    faiss.write_index(index, f"{INDEX_DIR}/faiss.index")
    with open(f"{INDEX_DIR}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return len(chunks)
