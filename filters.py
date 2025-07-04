# Semantic search UI
# filters.py
import streamlit as st
from vector import vectordb

def semantic_filter():
    st.title("🎯 Semantic Filter")
    query = st.text_input("Enter a topic or keyword to search in KB:")
    if query:
        with st.spinner("Searching knowledge base..."):
            results = vectordb.similarity_search_with_score(query, k=5)
            for doc, score in results:
                st.markdown(f"**Similarity Score:** {1 - score:.2f}")
                st.write(doc.page_content)
                st.markdown("---")
