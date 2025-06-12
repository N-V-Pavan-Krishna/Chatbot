# Firestore logging
# firebase.py
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_chat(user, user_input, bot_response):
    db.collection("chat_history").add({
        "user": user,
        "user_input": user_input,
        "bot_response": bot_response,
    })

def save_pdf_metadata(user, filename):
    db.collection("pdf_uploads").add({
        "user": user,
        "filename": filename,
    })
