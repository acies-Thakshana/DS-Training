import streamlit as st
import base64
import io
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key="AIzaSyB_-20eJsYiHZx1KVUFewyaL6AlEG60bHw")  

st.title("🖼️ Image Analysis")

def encode_image(image):
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG") 
    return base64.b64encode(img_bytes.getvalue()).decode("utf-8")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    encoded_image = encode_image(image)
    user_question = st.text_input("🔍 Ask a question about the image:")

    if user_question:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            user_question, 
            {"mime_type": "image/jpeg", "data": encoded_image}
        ])

        if response and hasattr(response, "text"):
            st.subheader("🤖 AI Answer:")
            st.write(response.text)
        else:
            st.error("⚠️ Unable to generate a response. Please try again.")
