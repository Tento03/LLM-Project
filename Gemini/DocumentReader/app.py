import time
import streamlit as st
import google.generativeai as genai
from pydantic.v1 import NoneStr
from api_key import api_key
import tempfile

genai.configure(api_key=api_key)

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    st.write("..All files are ready")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

st.title("File Reader")
st.subheader("An Application to help read the document")
prompt = st.text_input("Input Prompt")
uploaded_file = st.file_uploader('Upload your file', type=['pdf', 'docs', 'csv', 'xlsx'])
button = st.button('Submit')

if button:
    if uploaded_file is None:
        st.error("File is empty")
    elif prompt == "":
        st.error("Prompt is empty")
    else:
        files = [
            upload_to_gemini(uploaded_file, uploaded_file.type)
        ]
        wait_for_files_active(files)
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[0],
                        "Analyze the document\n",
                    ],
                },
            ]
        )
        response = chat_session.send_message(prompt)
        st.write(response.text)