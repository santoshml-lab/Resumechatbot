import streamlit as st
import pdfplumber
import requests

st.title("🤖 Resume Chatbot (API Version)")

# 🔑 HuggingFace API token (optional but recommended)
HF_API_KEY = "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"

API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def ask_api(question, context):
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# PDF extract
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

uploaded_file = st.file_uploader("Santosh_Yadav=Resume.pdf". type=["pdf"])

context = ""

if uploaded_file:
    context = extract_text(uploaded_file)
    st.success("Resume loaded ✅")

question = st.text_input("Ask question:")

if question and context:
    result = ask_api(question, context)

    if isinstance(result, list):
        st.success(result[0]["answer"])
    else:
        st.error("API Error or model loading... try again")

elif question:
    st.warning("Pehle resume upload karo 📄")
