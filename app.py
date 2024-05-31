import streamlit as st
import os
import textwrap
import google.generativeai as genai

# Function to display text as markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Set the Google API key
os.environ['GOOGLE_API_KEY'] = st.secrets['default']['API_KEY']

# Configure the GenerativeAI client
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Initialize the Streamlit app
st.title("Chatbot using Google's GenerativeAI")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get a response from the GenerativeAI API
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Extract the text from the response parts
    try:
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'text'):
                    return to_markdown(part.text)
                else:
                    st.write("No text found in part:", part)
        else:
            st.write("No parts found in the response.")
    except AttributeError as e:
        st.write(f"Error accessing response parts: {e}")

    # Handle the case where response.text might not be directly accessible
    try:
        if hasattr(response, 'text'):
            return to_markdown(response.text)
        else:
            st.write("No direct text found in the response.")
    except ValueError as e:
        st.write(f"Error accessing response text: {e}")

    return "Failed to generate a response."

# Text input for user prompt
user_input = st.text_input("You: ", "")

# Display conversation
if st.button("Send") and user_input:
    response = get_gemini_response(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display only the current message
if st.session_state.messages:
    last_message = st.session_state.messages[-1]
    st.markdown(f"**{last_message['role'].capitalize()}:** {last_message['content']}")

# Streamlit footer
st.markdown("---")
st.markdown("Chatbot built using [Streamlit](https://streamlit.io) and [Google's GenerativeAI](https://cloud.google.com).")
