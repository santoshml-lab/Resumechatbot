
import streamlit as st
import pdfplumber
from transformers import pipeline

st.set_page_config(page_title="Resume AI Bot", page_icon="🤖")

st.title("🤖 Resume AI Chatbot (Final Pro Version)")
st.write("Upload your resume and ask anything like a boss.")

# Load model safely
@st.cache_resource
def load_model():
    from transformers import pipeline
    return pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2"
    )

qa = load_model()

# PDF TEXT EXTRACTION (safe + fallback ready)
def extract_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        return ""

    return text

uploaded_file = st.file_uploader("Upload Resume (Santosh_Yadav_Resume.pdf)", type=["pdf"])

context = ""

if uploaded_file:
    context = extract_pdf(uploaded_file)

    if context.strip() == "":
        st.error("⚠️ PDF readable text nahi hai (scanned file ho sakta hai)")
        st.info("Tip: Word file se 'Save as text-based PDF' try karo")
    else:
        st.success("Resume loaded successfully ✅")

question = st.text_input("Ask your question:")

if question and context.strip():
    result = qa(question=question, context=context)

    st.markdown("### Answer:")
    st.success(result["answer"])

elif question:
    st.warning("Pehle resume upload karo 📄")
