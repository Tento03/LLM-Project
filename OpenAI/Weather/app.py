import streamlit as st
import  requests
import os
from openai import OpenAI
import google.generativeai as genai

def get_weather_data(city,weather_api_key):
    base_url=f"http://api.weatherapi.com/v1/forecast.json?"
    complete_url=base_url + "key=" + weather_api_key + "&q=" + city
    response=requests.get(complete_url)
    return response.json()

def generate_weather_description(data,openai_api_key):
    openai = OpenAI(
        # This is the default and can be omitted
        api_key=openai_api_key,
    )

    try:
        for temperature in data['forecast']['forecastday']:
            maxtemp = temperature['day']['maxtemp_c']
            description = temperature['day']['condition']['text']
            prompt=f"The current weather in your city is {description} with a temperature of {maxtemp:.1f}c. Explain this in a simple way for a general audience"

            response = openai.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
            return response.choices[0].message

    except Exception as e:
        return str(e)

def generate_description_with_gemini(gemini_api_key,data):
    genai.configure(api_key=gemini_api_key)
    try:
        for temperature in data['forecast']['forecastday']:
            maxtemp = temperature['day']['maxtemp_c']
            description = temperature['day']['condition']['text']
            prompt = f"The current weather in your city is {description} with a temperature of {maxtemp:.1f}c. Explain this in a simple way for a general audience"

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

            if 'chat_history' not in st.session_state:
                st.session_state['chat_history']=[]

            st.session_state['chat_history'].append({'role': 'user', 'parts': prompt})

            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            prompt,
                        ],
                    },
                ]
            )

            response = chat_session.send_message("Analyze the given prompt")
            st.session_state['chat_history'].append({'role': 'model', 'parts': response.text})
            # st.write(response.text)

            for chat in st.session_state['chat_history']:
                role='User' if chat['role']=='user' else 'Model'
                st.write(f"{role}: {chat['parts']}")
    except Exception as e:
        return str(e)

def main():
    st.sidebar.title("Weather Forecasting with LLM")
    city=st.sidebar.text_input("Enter city name","London")

    weather_api_key="c8c384ae10dd429d88d94059243010"
    openai_api_key="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"
    # "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"

    gemini_api_key="AIzaSyDG85tVy1-abeEr2ti06rnYsCYrJJPY_b0"
    submit=st.sidebar.button("Get Weather")

    if submit:
        st.title("Weather Updates For "+ city + " is:")
        with st.spinner("Fetching weather data.."):
            weather_data=get_weather_data(city,weather_api_key)

            for forecast in weather_data['forecast']['forecastday']:
                st.subheader(f"Tanggal: {forecast['date']}")
                st.write(f"Suhu Maksimum: {forecast['day']['maxtemp_c']}°C")
                st.write(f"Suhu Minimum: {forecast['day']['mintemp_c']}°C")
                st.write(f"Kondisi: {forecast['day']['condition']['text']}")
                st.write(f"Matahari Terbit: {forecast['astro']['sunrise']}")
                st.write(f"Matahari Terbenam: {forecast['astro']['sunset']}")

        weather_description=generate_weather_description(weather_data,openai_api_key)
        # st.write(weather_description)
        st.write(generate_description_with_gemini(gemini_api_key,weather_data))

if __name__=='__main__':
    main()
