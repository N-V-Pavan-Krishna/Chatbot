# app.py

import os
import streamlit as st
import sys
import types
import torch

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

# Monkey patching torch to avoid Streamlit inspect issues
sys.modules["torch.classes"] = types.ModuleType("torch.classes")
sys.modules["torch.classes"].__path__ = []
sys.modules["torch.__path__"] = None

os.environ["STREAMLIT_DISABLE_TELEMETRY"] = "1"
os.environ["XDG_CACHE_HOME"] = "/tmp"
os.environ["XDG_CONFIG_HOME"] = "/tmp"

# UI setup
st.set_page_config(page_title="Hybrid Chatbot", layout="wide")
st.title("💬 Google Services Support Chatbot")

query = st.text_input("Ask a question about Gemini or Google services:")
THRESHOLD = 0.75

@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

@st.cache_resource
def load_llm():
    pipe = pipeline("text2text-generation", model="google/flan-t5-small", max_new_tokens=256)
    return HuggingFacePipeline(pipeline=pipe)

# Load KB
vectordb = load_vectorstore()

# Process query
if query:
    with st.spinner("Processing..."):
        results = vectordb.similarity_search_with_score(query, k=1)
        if results:
            doc, distance = results[0]
            similarity = 1 - distance
            st.markdown(f"*Similarity Score:* {similarity:.2f}")
            if similarity > THRESHOLD:
                st.success("✅ Answer from knowledge base:")
                st.write(doc.page_content)
            else:
                st.warning("🤖 Not confident. Using LLM fallback...")
                llm = load_llm()
                response = llm.invoke(query)
                st.markdown(f"*LLM Answer:* {response}")
        else:
            st.warning("📂 No relevant document. Using LLM fallback...")
            llm = load_llm()
            response = llm.invoke(query)
            st.markdown(f"*LLM Answer:* {response}")
