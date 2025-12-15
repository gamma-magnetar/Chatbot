import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from openai import OpenAI

INDEX_DIR = "data/index"

client = OpenAI()

def load_index():
    index = faiss.read_index(f"{INDEX_DIR}/faiss.index")
    with open(f"{INDEX_DIR}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def answer_query(query, k=5):
    index, chunks = load_index()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)

    retrieved_chunks = [chunks[i] for i in I[0]]
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful assistant.
Answer the question strictly using the context below.
If the answer is not present, say "Information not found in the document."

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
