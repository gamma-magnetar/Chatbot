import pdfplumber
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ocr_utils import extract_images_and_ocr
from vision_utils import extract_vision_descriptions

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
    #text = extract_text_from_pdf(pdf_path)
    text = extract_text_from_pdf(pdf_path)
    ocr_text = extract_images_and_ocr(pdf_path)

    vision_text = ""

# Use vision if PDF is image-heavy
    if len(text.strip()) < 100:
       vision_text = extract_vision_descriptions(pdf_path)

    full_text = text + "\n" + ocr_text + "\n" + vision_text


    # 2. Extract charts/images text
    ocr_text = extract_images_and_ocr(pdf_path)

    full_text = text + "\n" + ocr_text

    # 3. Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(full_text)

    if len(chunks) == 0:
       raise ValueError(
           "No readable text found in the PDF. "
           "This PPT-based PDF likely contains only images or unsupported text."
       )


    # 4. Embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    if len(embeddings) == 0:
        raise ValueError("Embedding generation failed due to empty document content.")

    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(embeddings)) # type: ignore


    # 6. Persist index + chunks
    faiss.write_index(index, f"{INDEX_DIR}/faiss.index")
    with open(f"{INDEX_DIR}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return len(chunks)
