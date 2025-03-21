import streamlit as st
import base64
import io
from PIL import Image
from groq import Groq

# Secure API key storage
client = Groq(api_key="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")

st.title("🤖 AI Chatbot with Image Analysis (Groq)")
st.write("Chat with the AI or upload an image for analysis!")

# Sidebar for session management
with st.sidebar:
    st.header("💬 Chat Sessions")
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    if "current_session" not in st.session_state:
        st.session_state.current_session = "Session 1"
    session_names = list(st.session_state.chat_sessions.keys()) or ["Session 1"]
    selected_session = st.selectbox("Select Chat Session", session_names, index=session_names.index(st.session_state.current_session))
    st.session_state.current_session = selected_session
    if st.button("🆕 New Chat"):
        new_session_name = f"Session {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_session_name] = []
        st.session_state.current_session = new_session_name
        st.experimental_rerun()

if selected_session not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[selected_session] = []

for message in st.session_state.chat_sessions[selected_session]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me anything...")
if user_input:
    st.session_state.chat_sessions[st.session_state.current_session].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=200
    )
    bot_reply = response.choices[0].message.content
    st.session_state.chat_sessions[st.session_state.current_session].append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# Function to encode image to base64
def encode_image(image):
    img = Image.open(image)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG", quality=50)
    return base64.b64encode(img_bytes.getvalue()).decode("utf-8")

# Handle image upload
uploaded_file = st.file_uploader("Upload an image for analysis", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    encoded_image = encode_image(uploaded_file)
    user_question = st.text_input("Ask a question about the image:")
    if user_question:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_question},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]
        image_response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=messages,
            max_tokens=200
        )
        image_reply = image_response.choices[0].message.content
        st.session_state.chat_sessions[st.session_state.current_session].append({"role": "assistant", "content": image_reply})
        with st.chat_message("assistant"):
            st.markdown(image_reply)