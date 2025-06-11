#!/bin/bash

echo "🔧 Running setup.sh: Preloading FAISS index and models..."

# Build the FAISS index
python build_faiss.py

# Trigger model download so it's cached in image
python -c "from transformers import pipeline; pipeline('text2text-generation', model='google/flan-t5-small')"

echo "✅ setup.sh complete."
