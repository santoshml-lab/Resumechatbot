
import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from transformers import pipeline

st.title("🤖 Resume AI Chatbot (OCR Powered)")

@st.cache_resource
def load_model():
    from transformers import pipeline
    return pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2"
    )

qa = load_model()

uploaded_file = st.file_uploader("Upload Resume (Santosh_Yadav_Resume. pdf)", type=["pdf"])

context = ""

if uploaded_file:
    images = convert_from_bytes(uploaded_file.read())

    for img in images:
        text = pytesseract.image_to_string(img)
        context += text + "\n"

    if context.strip():
        st.success("Resume loaded successfully ✅")
    else:
        st.error("❌ Text extract nahi hua")

question = st.text_input("Ask question:")

if question and context.strip():
    result = qa(question=question, context=context)
    st.success(result["answer"])

elif question:
    st.warning("Pehle resume upload karo 📄")
