import streamlit as st
import os
from ingest import ingest_pdf
from rag import answer_query

st.set_page_config(page_title="PPT-PDF RAG Chatbot", layout="wide")

st.title("📊 PPT-PDF RAG Chatbot")
st.caption("Upload a PPT-based PDF and ask questions grounded in its content.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    os.makedirs("data/raw", exist_ok=True)
    pdf_path = f"data/raw/{uploaded_file.name}"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing PDF & building knowledge base..."):
        chunk_count = ingest_pdf(pdf_path)

    st.success(f"PDF processed successfully! ({chunk_count} chunks indexed)")

query = st.text_input("Ask a question based on the document")

if query:
    with st.spinner("Thinking..."):
        answer = answer_query(query)
    st.markdown("### 💡 Answer")
    st.write(answer)
