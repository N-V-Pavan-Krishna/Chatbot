# chains.py
from langchain.chains import ConversationalRetrievalChain
from langchain_google_vertexai import ChatVertexAI
from vector import vectordb
import vertexai

# Initialize Vertex AI with your project details
vertexai.init(
    project="hybrid-chatbot-kb",  # ⬅️ Replace this with your actual GCP Project ID
    location="us-central1"
)

def build_qa_chain():
    llm = ChatVertexAI(model="gemini-pro", temperature=0.2, convert_system_message_to_human=True)
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectordb.as_retriever())
