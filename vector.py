from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Initialize embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load or create the vector store
vectordb = Chroma(
    persist_directory="db",  # your path
    embedding_function=embedding_model
)
