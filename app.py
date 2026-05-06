import streamlit as st
import pdfplumber
from transformers import pipeline

st.set_page_config(page_title="Resume AI Chatbot", page_icon="🤖")

st.title("🤖 Resume AI Chatbot (Pro Version)")
st.write("Upload your resume and ask anything about it.")

# Load model safely
@st.cache_resource
def load_model():
    return pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2"
    )

qa = load_model()

# Extract PDF text
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Simple chunking (important for long resumes)
def chunk_text(text, size=800):
    return [text[i:i+size] for i in range(0, len(text), size)]

uploaded_file = st.file_uploader("Santosh_Yadav_Resume.pdf", type=["pdf"])

context_chunks = []

if uploaded_file:
    full_text = extract_text_from_pdf(uploaded_file)

    if full_text.strip() == "":
        st.error("PDF readable text nahi hai (maybe scanned image).")
    else:
        context_chunks = chunk_text(full_text)
        st.success("Resume loaded successfully ✅")

question = st.text_input("Ask your question:")

if question and context_chunks:
    best_answer = ""
    best_score = 0

    # search best chunk
    for chunk in context_chunks:
        result = qa(question=question, context=chunk)
        if result["score"] > best_score:
            best_score = result["score"]
            best_answer = result["answer"]

    st.markdown("### Answer:")
    st.success(best_answer)

elif question:
    st.warning("Pehle resume upload karo 📄")
