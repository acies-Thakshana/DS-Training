import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import base64
from groq import Groq
import cv2
import numpy as np
from PIL import Image

# Set up the Groq LLM for text-based chatbot and vision model
llm = ChatGroq(
    groq_api_key="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",  # Replace with your actual API key
    model_name="llama-3.2-11b-vision-preview",  # Model name for vision tasks
    temperature=0.7
)
client = Groq(api_key="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")

st.title("🤖 AI Chatbot with Image and Text Processing (Groq Only)")
st.write("Chat with the AI or upload an image for analysis!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to detect if the image is a color blindness test (Ishihara plate)
def detect_color_blind_test(image):
    """Determine if an image is a color blindness test (Ishihara plate)."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=100)
    return circles is not None

# Function to simulate color blindness
def simulate_color_blindness(image, type="protanopia"):
    """Apply color blindness filter based on type."""
    cb_matrices = {
        "protanopia": np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]]),
        "deuteranopia": np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]]),
        "tritanopia": np.array([[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]])
    }
    matrix = cb_matrices.get(type, cb_matrices["protanopia"])
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    transformed = np.dot(img / 255.0, matrix.T)
    transformed = (transformed * 255).clip(0, 255).astype(np.uint8)
    return cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB)

# Automatically process uploaded image
if uploaded_file:
    image = Image.open(uploaded_file)
    if image.mode == "RGBA":
        image = image.convert("RGB")
    img_array = np.array(image)
    image_path = "temp_image.jpg"
    image.save(image_path)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Encode image to base64 for Groq API
    encoded_image = encode_image(image_path)

    # Detect if the image is a color blindness test (Ishihara plate)
    is_color_blind_test = detect_color_blind_test(img_array)

    if is_color_blind_test:
        prompt = "Identify the number in this Ishihara color blindness test plate."
        blindness_types = ["protanopia", "deuteranopia", "tritanopia"]
        
        # Automatically simulate different types of color blindness
        for blindness_type in blindness_types:
            processed_img = simulate_color_blindness(img_array, blindness_type)
        
        # Send the processed image to Groq for analysis
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]}
        ]
    else:
        prompt = "Describe this image in detail, including objects, colors, and activities."
        
        # Send the image for general description to Groq
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]}
        ]

    # Send the request to Groq API
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=messages,
        max_tokens=200
    )

    # Show AI response
    answer = response.choices[0].message.content
    st.subheader("📝 AI Answer:")
    st.write(answer)
