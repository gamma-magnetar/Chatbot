import streamlit as st
import os
from ingest import ingest_pdf
from rag import answer_query

# -------------------------------
# Session state initialization
# -------------------------------
if "ingested" not in st.session_state:
    st.session_state.ingested = False

if "error" not in st.session_state:
    st.session_state.error = None

if "last_file" not in st.session_state:
    st.session_state.last_file = None

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="PPT-PDF RAG Chatbot", layout="wide")

st.title("📊 PPT-PDF RAG Chatbot")
st.caption("Upload a PPT-based PDF and ask questions grounded in its content.")

# -------------------------------
# File upload
# -------------------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# Reset state if a NEW file is uploaded
if uploaded_file and uploaded_file.name != st.session_state.last_file:
    st.session_state.ingested = False
    st.session_state.error = None
    st.session_state.last_file = uploaded_file.name

# -------------------------------
# PDF ingestion (runs ONCE per file)
# -------------------------------
if uploaded_file and not st.session_state.ingested and st.session_state.error is None:
    os.makedirs("data/raw", exist_ok=True)
    pdf_path = f"data/raw/{uploaded_file.name}"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing PDF & building knowledge base..."):
        try:
            chunk_count = ingest_pdf(pdf_path)
            st.session_state.ingested = True
            st.success(f"PDF processed successfully! ({chunk_count} chunks indexed)")
        except Exception as e:
            st.session_state.error = str(e)
            st.session_state.ingested = False

# -------------------------------
# Show ingestion error (once)
# -------------------------------
if st.session_state.error:
    st.error(st.session_state.error)

# -------------------------------
# Chat interface (enabled ONLY if ingested)
# -------------------------------
query = st.text_input(
    "Ask a question based on the document",
    disabled=not st.session_state.ingested
)

if query:
    with st.spinner("Thinking..."):
        answer = answer_query(query)
    st.markdown("### 💡 Answer")
    st.write(answer)
