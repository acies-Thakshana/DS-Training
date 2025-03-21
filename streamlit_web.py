import streamlit as st
import requests
from groq import Groq
import base64
from PIL import Image
import io
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# ============================#
# 🌟 Streamlit Page Config 🌟 #
# ============================#
st.set_page_config(page_title="InsightBot 🤖", layout="wide")

# Custom CSS for chat UI
st.markdown("""
    <style>
        /* Page Background */
        .main {
            background-color: #f8f9fa;
            padding: 20px;
        }

        /* Chat History Container */
        

        /* Chat Messages */
        .chat-container {
            padding: 12px;
            border-radius: 10px;
            margin: 8px 0;
            max-width: 80%;
        }
        .user-msg {
            background-color: #e8f5e9;
            padding: 12px;
            border-radius: 10px;
            margin-left: auto;
            max-width: 70%;
            color: black;
            text-align: left;
        }
        .ai-msg {
            background-color: #ffffff;
            padding: 12px;
            border-radius: 10px;
            max-width: 70%;
            color: black;
            text-align: left;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }

        /* Buttons - Highlighted in Yellow */
        .stButton>button {
            background-color: #FFD700 !important; /* Bright Yellow */
            color: black !important;
            font-size: 16px;
            padding: 12px 20px;
            border-radius: 8px;
            border: 2px solid black;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #FFC107 !important; /* Slightly darker yellow */
            color: black !important;
        }

        /* Upload Button - Yellow Highlight */
        .stFileUploader {
            border: 2px solid black !important;
            background-color: #FFF8DC !important; /* Light Yellow */
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }

        /* Input Boxes Highlight */
        .stTextArea textarea, .stTextInput input {
            border: 2px solid #FFD700 !important; /* Yellow Border */
            background-color: #FFFACD !important; /* Light Yellow */
            font-weight: bold;
            color: black;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #FFC107 !important;
            outline: none !important;
            box-shadow: 0px 0px 8px #FFD700 !important;
             border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)


st.title("InsightBot 🤖📸")
st.markdown("Chat with an AI assistant and get detailed descriptions of images! 🧠📷")

# ============================#
# 🤖 AI Setup (Groq for chat, BLIP for images) 🤖 #
# ============================#
API_KEY = "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"  # Replace with your valid Groq API key
client = Groq(api_key=API_KEY)

# Load BLIP model for image captioning
@st.cache_resource
def load_blip():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    return processor, model

processor, model = load_blip()

# ============================#
# 💬 Chatbot Section 💬 #
# ============================#
st.subheader("💬 Chat with AI")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Display chat history in a scrollable container
st.markdown('<div class="chat-history">', unsafe_allow_html=True)

for chat in st.session_state.chat_history:
    role = "👤 You" if chat["role"] == "user" else "🤖 AI"
    msg_class = "user-msg" if chat["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="chat-container {msg_class}"><b>{role}:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input box (moves down on new input)
user_input = st.text_area("Type your message and press Enter:", key="user_input")

if st.button("Send"):
    if user_input.lower() == "stop":
        st.write("🚀 Conversation ended.")
        st.stop()

    with st.spinner("🤖 AI is thinking..."):
        try:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            chat_response = client.chat.completions.create(
                model="llama3-8b-8192",  # Using an available model
                messages=st.session_state.chat_history,
                max_tokens=300,
                temperature=0.7
            )
            response_text = chat_response.choices[0].message.content

            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"Error: {e}")

# ============================#
# 📸 Image Upload & Description (BLIP) 📸 #
# ============================#
st.subheader("📸 Upload an Image for AI Description")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


    with st.spinner("🖼️ AI is analyzing the image..."):
        try:
            # Process image for BLIP
            inputs = processor(image, return_tensors="pt")

            # Generate a detailed caption
            with torch.no_grad():
                out = model.generate(**inputs, max_length=100, do_sample=True, temperature=0.7)
                description = processor.decode(out[0], skip_special_tokens=True)

            # Convert single-line response to paragraph format
            formatted_description = "\n\n".join(description.split(". "))

            st.subheader("📝One liner about the image")
            st.write(formatted_description)

        except Exception as e:
            st.error(f"Error: {e}")

# ============================#
# 🖼️ Image-Based Q&A (Vision Model) 🖼️ #
# ============================#
st.subheader("Hey!Wanna know about the image")

# Function to encode image to base64
# Function to encode image to base64 (Fixes RGBA to RGB conversion)
def encode_image(image):
    if image.mode == "RGBA":
        image = image.convert("RGB")  # Convert RGBA to RGB to avoid JPEG errors
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


if uploaded_file:
    user_question = st.text_input("Ask a question about the image:")

    if user_question:
        try:
            # Convert image to base64
            encoded_image = encode_image(image)

            # Prepare prompt with image and user question
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                    ]
                }
            ]

            # Send request to Groq AI (using available vision model)
            response = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",  # Adjust this if another vision model is available
                messages=messages,
                max_tokens=200
            )

            # Show AI response
            answer = response.choices[0].message.content
            st.subheader("📝 AI Answer:")
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")
