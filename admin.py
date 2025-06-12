# Admin view for chat logs
# admin.py
import streamlit as st
import pandas as pd
from firebase import db

def admin_view():
    st.title("📜 Chat History Admin Panel")

    chats = db.collection("chat_history").stream()
    rows = []
    for chat in chats:
        data = chat.to_dict()
        rows.append((data["user"], data["user_input"], data["bot_response"]))

    if rows:
        df = pd.DataFrame(rows, columns=["User", "User Input", "Bot Response"])
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="chat_history.csv")
    else:
        st.info("No chat logs found.")
