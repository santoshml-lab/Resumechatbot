
from transformers import pipeline
import gradio as gr
from pypdf import PdfReader

# load resume
reader = PdfReader("Santosh_Yadav_Resume.pdf")
resume_text = ""
for page in reader.pages:
    resume_text += page.extract_text()

qa = pipeline("question-answering")

def chatbot(question):
    result = qa(
        question=question,
        context=resume_text[:2000]
    )
    answer = result['answer']
    
    if len(answer.strip()) < 3:
        return "This info is not in my resume."
    
    return "👉 " + answer

iface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(placeholder="Ask about my skills..."),
    outputs="text",
    title="AI Resume Chatbot"
)

iface.launch(server_name="0.0.0.0", server_port=7860)
