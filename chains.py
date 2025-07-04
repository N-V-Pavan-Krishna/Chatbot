import logging
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from vector import vectordb
import google.generativeai as genai
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_qa_chain():
    """Build a production QA chain using Gemini via Generative AI SDK"""
    try:
        if vectordb is None:
            raise Exception("Vector database not initialized.")
        
        # Set your API key
        os.environ["GOOGLE_API_KEY"] = "<your_api_key>"

        # Configure genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

        logger.info("Building QA chain with Gemini (genai)...")

        # Use LangChain's wrapper for Generative AI
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-001",  # or gemini-1.5-pro
            temperature=0.7,
            max_output_tokens=1024
        )

        retriever = vectordb.as_retriever()

        system_prompt = (
            "You are an assistant for answering questions about Gemini and Google services. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say you don't know — don't make anything up. "
            "Be concise and clear.\n\nContext:\n{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        doc_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
        rag_chain = create_retrieval_chain(retriever, doc_chain)

        logger.info("Gemini QA chain (genai) built successfully.")
        return rag_chain

    except Exception as e:
        logger.error(f"Error building Gemini QA chain: {e}")
        raise RuntimeError(f"Failed to build Gemini QA chain: {e}")
