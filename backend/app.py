import streamlit as st
from translate3 import native_support
from tts import financial_tips_agent
from rag import graph
import os
import importlib

stt_module = importlib.import_module("stt")
transcription = stt_module.transcription

# Streamlit App Configuration
st.set_page_config(page_title="Loan & Financial Assistant", layout="wide")

# Sidebar for User Input
st.sidebar.title("Loan & Financial Assistant")
st.sidebar.write("Select your input method and language.")

# Language Selection
language_options = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN"
}
language_choice = st.sidebar.selectbox("Select Language", list(language_options.keys()))
language_code = language_options[language_choice]

# Input Selection: Voice or Text
input_method = st.sidebar.radio("Choose Input Method:", ("Voice Input", "Text Input"))

user_query = ""
if input_method == "Text Input":
    user_query = st.text_area("Enter your query:")
elif input_method == "Voice Input":
    if st.button("Record Voice (10s)"):
        st.write("Recording... Speak now!")
        user_query = transcription
        st.write(f"Transcription: **{user_query}**")

# Processing Query with RAG Model
if st.button("Get Response"):
    if user_query:
        state = {"messages": [{"content": user_query}]}
        result = graph.invoke(state)
        response_text = result["messages"][-1].content

        # Translation to Native Language
        native_response = native_support(response_text)

        # Display Output
        st.subheader("Response:")
        st.write(response_text)

        # Convert to Speech
        audio_file_path = financial_tips_agent(native_response)

        # Play Audio Output
        st.audio(audio_file_path)

    else:
        st.warning("Please provide input via text or voice.")

# Run the Streamlit App
if __name__ == "__main__":
    st.write("Welcome to the Loan & Financial Assistant!")
