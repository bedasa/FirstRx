import streamlit as st
from google.cloud importaiplatformv1beta1 as gapiclient

# Replace with your Gemini API key
API_KEY = "AIzaSyBcbUSkMPUYpdu9f8QdH46voXl0z84TQCY"

# Function to generate response using Gemini
def generate_response(prompt, context):
  """Sends user prompt and context to Gemini for response generation."""
  endpoint = gapiclient.Endpoint.create(location="us-central1")
  project = "projects/YOUR_PROJECT_ID"  # Replace with your project ID
  location = endpoint.location
  locations = gapiclient.ListLocationsRequest(parent="projects/YOUR_PROJECT_ID")  # Replace with your project ID
  for location in gapiclient.LocationServiceClient().ListLocations(locations).locations:
    if location.name == location:
      break

  service = gapiclient.TextGenerationServiceClient(client_options={"api_key": API_KEY})
  request = gapiclient.GenerateTextRequest(
      parent=f"{project}/locations/{location}",
      text_input=gapiclient.TextInput(text=prompt, previous_chat_messages=context),
  )
  response = service.generate_text(request=request)
  return response.generated_text[0].text

# Initialize chat history
chat_history = []

st.title("Streamlit Chatbot with Gemini")

# Input field for user prompt
user_input = st.text_input("You: ")

# Send prompt to Gemini and get response
if user_input:
  # Add user input to chat history
  chat_history.append({"speaker": "User", "text": user_input})

  # Generate response using Gemini
  response = generate_response(user_input, chat_history)

  # Add Gemini response to chat history
  chat_history.append({"speaker": "Gemini", "text": response})

  # Display chat history
  for message in chat_history:
    st.write(f"{message['speaker']}: {message['text']}")

