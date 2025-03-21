import streamlit as st
import requests
from groq import Groq
from PIL import Image
import base64
import io

API_KEY = "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"  
client = Groq(api_key=API_KEY)

st.title("🖼️ AI Image Description Bot 🤖")

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Upload image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save file locally
    image_path = "temp_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Convert image to base64
    encoded_image = encode_image(image_path)

    # Prepare the prompt for AI
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]
        }
    ]

    # Send request to Groq AI
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",  # Use Groq's vision model
        messages=messages,
        max_tokens=200
    )

    # Show AI response
    description = response.choices[0].message.content
    st.subheader("📝 AI Description:")
    st.write(description)