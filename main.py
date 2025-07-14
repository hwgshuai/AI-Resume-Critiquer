import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI PDF Summarizer", page_icon="📖", layout="centered")

st.title("AI Resume Critiquer")

st.markdown("""
    This app summarizes your resume using AI.
""")

st.text("hello")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

uploader_files = st.file_uploader("Upload your resume here:", type=["pdf","txt"])

job_role = st.text_input("What role are you applying for?")

analyze = st.button("Analyze")

def extract_pdf(uploader_files):
    pdfReader = PyPDF2.PdfReader(uploader_files)
    text = ""
    for page in pdfReader.pages:
        text += page.extract_text() + "\n"
    return text
def extract_file(uploader_files):
    if uploader_files.type == "application/pdf":
        return extract_pdf(io.BytesIO(uploader_files.read()))
    elif uploader_files.type == "text/plain":
        return uploader_files.read().decode("utf-8")

if analyze and uploader_files:
    st.text("button pressed")
    try:
        file_content = extract_file(uploader_files)

        if not file_content.strip():
            st.error("The uploaded file is empty.")
            st.stop

        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}

        Please provide your analysis in a clear, structured format with specific recommendations."""

        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"  # DeepSeek 的兼容 API 入口
        )

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=1.3,
            max_tokens=512,
        )

        st.markdown("###the analysis results:")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {e}")

