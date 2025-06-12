# app.py
import os
import streamlit as st
import sys
import types

from auth import login
from chains import build_qa_chain
from memory import memory
from firebase import save_chat
from admin import admin_view
from upload import upload_pdfs
from filters import semantic_filter

# Fix torch Streamlit inspection issue
sys.modules["torch.classes"] = types.ModuleType("torch.classes")
sys.modules["torch.classes"].__path__ = []
sys.modules["torch.__path__"] = None

# Streamlit setup
os.environ["XDG_CACHE_HOME"] = "/tmp"
os.environ["XDG_CONFIG_HOME"] = "/tmp"
st.set_page_config(page_title="Hybrid Chatbot", layout="wide")

# Auth
authenticator, name, auth_status, username, role = login()

if auth_status:
    authenticator.logout("Logout", location="sidebar")
    st.title(f"💬 Welcome, {name}!")

    qa_chain = build_qa_chain()
    query = st.chat_input("Ask a question about Gemini or Google services:")

    with st.expander("🧠 Conversation Memory"):
        for msg in memory.chat_memory.messages:
            role_display = "👤 You" if msg.type == "human" else "🤖 Bot"
            st.markdown(f"**{role_display}:** {msg.content}")

    if query:
        with st.spinner("Thinking..."):
            try:
                chat_history = memory.chat_memory.messages if memory.chat_memory.messages else []
                response = qa_chain.invoke({
                    "question": query,
                    "chat_history": chat_history
                })
                st.success("✅ Gemini Answer:")
                st.write(response)
                save_chat(username, query, response)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    with st.sidebar:
        st.markdown("## 🛠 Tools")
        if role == "admin":
            if st.button("📜 Admin Panel"):
                admin_view()
        if st.button("📤 Upload PDFs"):
            upload_pdfs(username)
        if st.button("🎯 Filter KB"):
            semantic_filter()

elif auth_status == False:
    st.error("Invalid credentials")
elif auth_status == None:
    st.warning("Please enter your username and password")
