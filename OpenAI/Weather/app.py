import time
import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyAGHWCWhiFkXLgovxFdDWw3DvsBrBNcCBk")

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

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

st.title("Audio Analytics")
st.subheader("An Application For Voice Analytics")

# Input voice
voice = st.experimental_audio_input("Record your voice")
uploaded_files = st.file_uploader("Upload a voice file", type=['ogg', 'mp3', 'aac', 'wav', 'm4a'])
submit_button = st.button("SUBMIT")

if submit_button:
    if voice is None and uploaded_files is None:
        st.error("Please provide a voice input or upload a file.")
    else:
        if uploaded_files is not None:
            file = upload_to_gemini(uploaded_files, mime_type=uploaded_files.type)
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [file],
                    },
                ]
            )
        else:  # voice input
            file = upload_to_gemini(voice, mime_type='audio/ogg')  # Update mime type as needed
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [file],
                    },
                ]
            )

        response = chat_session.send_message("Answer his question")
        st.write(response.text)
