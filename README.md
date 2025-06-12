# Hybrid Chatbot with Vertex AI + ChromaDB + Streamlit

This project is a **Google Services Support Chatbot** that uses:

* **Vertex AI Gemini** for fallback LLM
* **ChromaDB** for storing and retrieving knowledge base embeddings
* **Streamlit Authenticator** for login with role-based views
* **Firebase Firestore** for chat logging
* **PDF Uploading** to ingest content into the knowledge base

---
## Prerequisites

1. **Google Cloud Project**

   * Vertex AI API must be enabled
   * Billing must be enabled
2. **Service Account** with role `Vertex AI User`

   * Download the JSON key (e.g., `gcp_key.json`)
3. **Python 3.10 or above**

---

## Setup Instructions

### 1.Clone the Project

```bash
cd hybrid_chatbot_KB
```

## 2.Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # For Windows
```

## 3.Install Requirements

```bash
pip install -r requirements.txt
```

## 4.Add Your GCP Service Account Key

Save your downloaded JSON as:

```
gcp_key.json
```

## 5.Set Environment Variable (every time you start)

**For PowerShell:**

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="gcp_key.json"
```

**For CMD:**

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=gcp_key.json
```

Or use `run_chatbot.bat` to automate it.

---

## Running the App

```bash
streamlit run app.py
```

## Login Details (Default)

| Username | Password  | Role  |
| -------- | --------- | ----- |
| pavan    | 1234      | user  |
| admin    | adminpass | admin |

You can update users in `auth.py` with your own hashed passwords.

## Features

* Ask questions about uploaded PDFs or Gemini fallback
* Upload PDFs → processed via `upload.py`
* Admin can view full chat logs
* Filter KB via semantic vector search
* Chat memory support included

## Directory Structure
.
├── app.py              # Main Streamlit app
├── auth.py             # Login & roles
├── admin.py            # Admin chat logs view
├── upload.py           # PDF upload handler
├── firebase.py         # Firestore logging
├── filters.py          # Semantic search tools
├── chains.py           # Gemini + Retriever QA chain
├── memory.py           # LangChain memory store
├── vector.py           # ChromaDB vector store setup
├── gcp_key.json        # GCP service account key (not committed)
├── requirements.txt    # Python dependencies
└── .streamlit/secrets.toml # (if using Streamlit secrets)
```

#Deployment Options

* Run locally via VS Code or terminal
* Deploy to Google Cloud Run, App Engine, or Vertex AI Workbench with some tweaks
