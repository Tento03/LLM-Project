import streamlit as st
import  time
import google.generativeai as genai

api_key="AIzaSyDrcXBfGIyas8f0GyD1nPYlm2FylqoMWN8"

genai.configure(api_key=api_key)

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  st.write("Waiting for file to processing")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

st.title("Aplikasi abal abal")
st.subheader("Benar")
prompt=st.text_input("Input")
uploader=st.file_uploader("Upload",type=['pdf','docs'])
submits=st.button("Submit")

if submits:
    if uploader is not None:
        files = [
            upload_to_gemini(uploader, mime_type=uploader.type),
        ]
        # Some files have a processing delay. Wait for them to be ready.
        with st.spinner("Wait for it"):
            time.sleep(10)
            st.write("All files are ready")
            st.write()
            wait_for_files_active(files)


        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[0],
                    ],
                },
            ]
        )

        response = chat_session.send_message(prompt)
        st.write(response.text)
