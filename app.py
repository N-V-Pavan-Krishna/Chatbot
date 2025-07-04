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

sys.modules["torch.classes"] = types.ModuleType("torch.classes")
sys.modules["torch.classes"].__path__ = []
sys.modules["torch.__path__"] = None

os.environ["XDG_CACHE_HOME"] = "/tmp"
os.environ["XDG_CONFIG_HOME"] = "/tmp"
st.set_page_config(page_title="Hybrid Chatbot", layout="wide")

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
                # create_retrieval_chain expects {"input": query}
                response = qa_chain.invoke({"input": query})
                
                # Extract the answer from the response dictionary
                if isinstance(response, dict) and "answer" in response:
                    answer = response["answer"]
                else:
                    # Fallback if response format is unexpected
                    answer = str(response)

                st.success("✅ Gemini Answer:")
                st.write(answer)

                # Save to memory and database
                memory.chat_memory.add_user_message(query)
                memory.chat_memory.add_ai_message(answer)
                save_chat(username, query, answer)

                # Optional: Show source documents if available
                if isinstance(response, dict) and "context" in response:
                    with st.expander("📚 Source Documents"):
                        for i, doc in enumerate(response["context"]):
                            st.write(f"**Source {i+1}:**")
                            # Show first 500 characters of each document
                            content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                            st.write(content[:500] + "..." if len(content) > 500 else content)
                            
                            # Show metadata if available
                            if hasattr(doc, 'metadata') and doc.metadata:
                                st.write(f"*Metadata: {doc.metadata}*")
                            st.write("---")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                # Optional: Show more detailed error for debugging
                if st.checkbox("Show detailed error (for debugging)"):
                    st.exception(e)

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