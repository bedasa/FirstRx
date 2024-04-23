import streamlit as st
#from google.ai import generativelanguage_v1beta as gapiclient
import google.generativeai as ggi


# Input google API key
user_input_google_project_api_key= st.text_input("Input Google Project API Key: ")

ggi.configure(api_key = user_input_google_project_api_key)

model = ggi.GenerativeModel("gemini-pro") 
chat = model.start_chat()

def LLM_Response(question):
    response = chat.send_message(question,stream=True)
    return response

st.title("First RxChat ..... Developed by Team Agranika using Gemini Pro")


user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = LLM_Response(user_quest)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)