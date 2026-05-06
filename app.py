
import streamlit as st
import pdfplumber
from transformers import pipeline

st.set_page_config(page_title="Resume AI Bot", page_icon="🤖")

st.title("🤖 Resume Chatbot")

# Model load
@st.cache_resource
def load_model():
    from transformers import pipeline
    return pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2"
    )

qa = load_model()

# SESSION STATE FIX (MOST IMPORTANT)
if "context" not in st.session_state:
    st.session_state.context = ""

# FILE UPLOAD
uploaded_file = st.file_uploader("Upload Resume (Santosh_Yadav_Resume.pdf)", type=["pdf"])

# DEBUG VISIBILITY (IMPORTANT)
if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        st.session_state.context = text

        if text.strip() == "":
            st.error("⚠️ PDF se text extract nahi ho raha (scanned file ho sakta hai)")
        else:
            st.success("Resume loaded successfully ✅")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# SHOW CONTEXT DEBUG (IMPORTANT)
st.write("DEBUG - Context Length:", len(st.session_state.context))

# QUESTION INPUT
question = st.text_input("Ask question:")

if question and st.session_state.context:
    result = qa(question=question, context=st.session_state.context)
    st.success(result["answer"])

elif question:
    st.warning("Pehle resume upload karo 📄")
