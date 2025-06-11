# build_faiss.py

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

loader = TextLoader(r"C:\Users\user\Downloads\google_chatbot\google_chatbot\google_chatbot\google_kb.txt")
documents = loader.load()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(documents, embeddings)
db.save_local("faiss_index")
