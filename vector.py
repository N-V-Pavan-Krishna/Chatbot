# Embeddings + ChromaDB vector store
# vector.py
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="chroma_store", embedding_function=embedding_model)

# Create if not exists
if not os.path.exists("chroma_store"): os.makedirs("chroma_store")
