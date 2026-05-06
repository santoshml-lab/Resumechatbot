import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resume Chatbot", page_icon="🤖")

st.title("🤖 Resume Chatbot (PDF AI)")

@st.cache_resource
def load_model():
    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad"
    )

qa = load_model()

uploaded_file = st.file_uploader("Santosh_Yadav_Resume.pdf", type=["pdf"])

context = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            context += text

    st.success("Resume loaded ✅")

question = st.text_input("Ask question:")

if question and context:
    result = qa(question=question, context=context)
    st.success(result["answer"])

elif question:
    st.warning("Pehle resume upload karo 📄")
