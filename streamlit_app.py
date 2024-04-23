import streamlit as st
from google.cloud import aiplatform_v1 as gapiclient

# Replace with your Gemini API key
API_KEY = "AIzaSyBcbUSkMPUYpdu9f8QdH46voXl0z84TQCY"

# Function to generate response using Gemini
def generate_response(prompt, context, user_input_google_project, user_input_google_project_api_key):
  """Sends user prompt and context to Gemini for response generation."""
  endpoint = gapiclient.Endpoint.create(location="us-central1")
  project = "projects/"+user_input_google_project  # Replace with your project ID
  location = endpoint.location
  locations = gapiclient.ListLocationsRequest(parent="projects/"+user_input_google_project)  # Replace with your project ID
  for location in gapiclient.LocationServiceClient().ListLocations(locations).locations:
    if location.name == location:
      break

  service = gapiclient.TextGenerationServiceClient(client_options={"api_key": user_input_google_project_api_key})
  request = gapiclient.GenerateTextRequest(
      parent=f"{project}/locations/{location}",
      text_input=gapiclient.TextInput(text=prompt, previous_chat_messages=context),
  )
  response = service.generate_text(request=request)
  return response.generated_text[0].text

# Initialize chat history
chat_history = []

st.title("Streamlit Chatbot Developed by Agranika team with Gemini")


# Input google project and API key
user_input_google_project = st.text_input("Input Google Project ID: ")
user_input_google_project_api_key= st.text_input("Input Google Project API Key: ")


# Input field for user prompt
user_input = st.text_input("You: ")

# Send prompt to Gemini and get response
if user_input:
  # Add user input to chat history
  chat_history.append({"speaker": "User", "text": user_input})

  # Generate response using Gemini
  response = generate_response(user_input, chat_history, user_input_google_project, user_input_google_project_api_key)

  # Add Gemini response to chat history
  chat_history.append({"speaker": "Gemini", "text": response})

  # Display chat history
  for message in chat_history:
    st.write(f"{message['speaker']}: {message['text']}")

