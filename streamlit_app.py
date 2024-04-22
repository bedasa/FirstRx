import streamlit as st
from audiorecorder import audiorecorder
import google.generativeai as genai

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

GOOGLE_API_KEY="AIzaSyB8yQqUaXoXlkrPO8Bw6y5k-lOakRBNXfk"

genai.configure(api_key=GOOGLE_API_KEY)

st.title("Audio Recorder")

audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.export().read())  

    # To save audio to a file, use pydub export method:
    audio.export("audio.wav", format="wav")

    def generate():
        vertexai.init(project="streamlit-420019", location="us-central1")
       

        video1 = Part.from_uri(
            mime_type="audio/wav",
            uri="https://storage.cloud.google.com/audio-file-analysis/audio.wav")
        text1 = """Analyze the audio carefully and perform a Named Entity Recognition assuming a
        person is giving his/her introduction whith symptoms of illness. The output should be in a JSON
        format only.Only base your answers strictly on what information is available in the audio attached.
        Do not make up any information that is not part of the audio and do not be too verbose.
        """

        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        model = GenerativeModel("gemini-1.5-pro-preview-0409")
        responses = model.generate_content(
            [video1, text1],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )

        for response in responses:
            print(response.text, end="")

    generate()



        # To get audio properties, use pydub AudioSegment properties:
        #st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

