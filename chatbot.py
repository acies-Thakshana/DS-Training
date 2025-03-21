import streamlit as st
from groq import Groq

# Set up the Groq API key
API_KEY = "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"  # Replace with your actual API key
client = Groq(api_key=API_KEY)

# Streamlit UI
st.title("🤖 Groq AI Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send full chat history to Groq API
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages,  # ✅ Send full chat history
        max_tokens=300  # Adjust token limit as needed
    )

    # Extract AI response
    ai_message = response.choices[0].message.content

    # Append AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_message})

    # Re-render updated chat history
    st.rerun()
