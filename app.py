
import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader

# Load model
qa = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

st.set_page_config(page_title="Resume Chatbot", page_icon="🤖")

st.title("🤖 Resume Chatbot (PDF Upload)")
st.write("Upload your resume and ask questions like a pro.")

# PDF upload
uploaded_file = st.file_uploader("Santosh_Yadav_Resume.pdf", type=["pdf"])

context = ""

# Extract text from PDF
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        context += page.extract_text()

    st.success("Resume loaded successfully ✅")

# Ask question
question = st.text_input("Ask your question:")

if question and context:
    result = qa(question=question, context=context)
    st.markdown("### Answer:")
    st.success(result["answer"])

elif question and not context:
    st.warning("Please upload your resume first 📄")
