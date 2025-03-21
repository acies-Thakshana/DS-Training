import streamlit as st
import requests
from groq import Groq
import base64
from PIL import Image
import io

API_KEY = "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"  
client = Groq(api_key=API_KEY)

st.title("Image Question Answering Bot")

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

    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64
    encoded_image = encode_image(image_path)

    # Ask the user a question about the image
    user_question = st.text_input("Ask a question about the image:")

    if user_question:
        # Prepare the prompt for AI (including both image and the user's question)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_question},  # User's question
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]

        # Send request to Groq AI (vision model)
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview", 
            messages=messages,
            max_tokens=200
        )

        # Show AI response
        answer = response.choices[0].message.content
        st.subheader("📝 AI Answer:")
        st.write(answer)