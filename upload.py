from langchain_community.document_loaders import PyPDFLoader
from vector import vectordb
import streamlit as st

def upload_pdfs(username):
    uploaded_files = st.file_uploader("Upload PDF(s)", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.read())
            loader = PyPDFLoader(uploaded_file.name)
            docs = loader.load()
            vectordb.add_documents(docs)
            st.success(f"✅ Uploaded and embedded {uploaded_file.name}")