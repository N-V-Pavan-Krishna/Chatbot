# PDF uploading and embedding
# upload.py
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from vector import vectordb
from firebase import save_pdf_metadata

def upload_pdfs(username):
    st.title("📤 Upload PDF Files")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        for pdf in uploaded_files:
            loader = PyPDFLoader(pdf)
            pages = loader.load_and_split()
            vectordb.add_documents(pages)
            save_pdf_metadata(username, pdf.name)
        st.success("✅ Upload & Embedding Complete")
