import streamlit as st
import google.generativeai as genai
from api_key import api_key
import tempfile

genai.configure(api_key=api_key)


def upload_to_gemini(path, mime_type=None):
  # Save the uploaded file to a temporary file
  with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
    temp_file.write(path.read())
    temp_file_path = temp_file.name

  # Upload the temporary file
  file = genai.upload_file(temp_file_path, mime_type=mime_type)
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

st.set_page_config(page_title="Image Analytics", page_icon=":robot:")
st.image("onepiece.png", width=200)
st.title("Image Analytics")
st.subheader("An Application to Generate Text from Given Images")

uploaded_files=st.file_uploader("Upload image",type=['png','jpg','jpeg'])
submitbutton=st.button("Generate Text")

if submitbutton:
  if uploaded_files is None:
    st.error("Image is empty")
  else:
    files = [
      upload_to_gemini(uploaded_files, mime_type=uploaded_files.type),
    ]
    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            files[0],
            "analyze this image\n",
          ],
        },
      ]
    )
    response = chat_session.send_message( f"Analyze the uploaded image and provide a detailed analysis and translate to Indonesia.")
    st.write(response.text)