import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Models
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to generate a caption using BLIP-2
def generate_caption(image):
    inputs = processor(image, return_tensors="pt")
    output = blip_model.generate(**inputs)
    return processor.decode(output[0], skip_special_tokens=True)

# Function to refine the description using Groq
def refine_description(caption):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Groq-supported model
        messages=[
            {"role": "system", "content": "You are an AI that enhances image captions with details."},
            {"role": "user", "content": f"Refine this caption and provide more details: {caption}"}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("🖼️ Image-to-Text with Groq & BLIP-2")
st.write("Upload an image, and AI will generate a detailed description.")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Description"):
        caption = generate_caption(image)
        final_description = refine_description(caption)

        st.subheader("AI Generated Description:")
        st.write(final_description)

