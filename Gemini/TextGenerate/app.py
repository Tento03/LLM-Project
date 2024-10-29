import streamlit as st
import google.generativeai as genai
from api_key import api_key

genai.configure(api_key=api_key)

def upload_to_gemini(prompt):
    print(f"Prompt: {prompt}")
    return prompt

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

st.title("Generated Text")
st.subheader("An Application to Generate Text")

# Input dari pengguna
prompt = st.chat_input("Say Something")

if prompt:  # Jika ada input
    uploaded_prompt = upload_to_gemini(prompt)

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    uploaded_prompt,
                    "Generate text\n",
                ],
            },
        ]
    )
    response = chat_session.send_message("Generate Text based on the input prompt")
    st.text_area("Generated Response", value=response.text, height=300)
else:
    st.write("Text is empty")
