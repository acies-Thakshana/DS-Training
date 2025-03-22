import streamlit as st
from groq import Groq

# Set up the Groq API key
API_KEY = "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"  
client = Groq(api_key=API_KEY)

# Streamlit UI
st.set_page_config(page_title="Groq AI Chatbot", layout="wide")
st.title("💬 Groq AI Chatbot 🤖")

# Sidebar for chat history
st.sidebar.title("Chat History")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history in sidebar
for message in st.session_state.messages:
    if message["role"] == "user":
        st.sidebar.markdown(f"**You:** {message['content']}")
    else:
        st.sidebar.markdown(f"**AI:** {message['content']}")

# Display chat in main UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me anything...")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Groq API
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages
    )

    # Extract AI response
    ai_message = response.choices[0].message.content

    # Add AI message to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_message})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_message)