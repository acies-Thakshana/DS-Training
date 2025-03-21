import streamlit as st
from groq import Groq

# Sidebar for API Key input (optional, if you want it to be dynamic)
st.sidebar.title("🔑 Settings")
API_KEY = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Ensure the API key is provided
if not API_KEY:
    st.sidebar.warning("⚠️ Please enter your API key to proceed.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Streamlit UI
st.title("🤖 Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with different avatars
for message in st.session_state.messages:
    role = message["role"]
    avatar = "👤" if role == "user" else ""
    with st.chat_message(role):
        st.markdown(f"{avatar} **{role.capitalize()}**: {message['content']}")
    st.divider()  # ✅ Adds a visual separation for better readability

# User input field
user_input = st.chat_input("Ask something...")

if user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Send full conversation history to Groq AI
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # ✅ Ensure you're using an available model
            messages=st.session_state.messages,
            max_tokens=300
        )

        # Get AI's response
        ai_response = response.choices[0].message.content

        # Append AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # Re-run to refresh the chat
        st.rerun()

    except Exception as e:
        # If the API call fails (e.g., due to an incorrect API key), show an error message
        st.error(f"⚠️ Error: {str(e)}. Please check your API key.")
        st.stop()  # Stop execution to prevent further errors
