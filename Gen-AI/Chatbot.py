import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import base64
from groq import Groq

# Set up the Groq LLM for text-based chatbot and vision model
llm = ChatGroq(
    groq_api_key="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",  # Replace with your actual API key
    model_name="llama-3.2-11b-vision-preview",  # This should be the model name for vision tasks
    temperature=0.7
)
client = Groq(api_key="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")

# Define chatbot prompt template
text_prompt = ChatPromptTemplate.from_messages([ 
    ("system", "You are a helpful AI Assistant."),
    ("user", "{question}")
])

# Streamlit UI
st.title("🤖 AI Chatbot with Image and Text Processing (Groq Only)")
st.write("Chat with the AI or upload an image for analysis!")

# Sidebar for session management
with st.sidebar:
    st.header("💬 Chat Sessions")

    # Initialize multiple chat sessions
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}  # Store multiple chat histories
    if "current_session" not in st.session_state:
        st.session_state.current_session = "Session 1"  # Default session

    # Dropdown to switch sessions
    session_names = list(st.session_state.chat_sessions.keys()) or ["Session 1"]
    selected_session = st.selectbox("Select Chat Session", session_names, index=session_names.index(st.session_state.current_session))

    # Update current session
    st.session_state.current_session = selected_session

    # Button to create a new chat session
    if st.button("🆕 New Chat"):
        new_session_name = f"Session {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[new_session_name] = []  # Create new session
        st.session_state.current_session = new_session_name  # Switch to new session
        st.rerun()  # Refresh UI to reflect changes

# Initialize chat history for selected session
if selected_session not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[selected_session] = []

# Display chat history for the current session (latest at bottom)
for message in reversed(st.session_state.chat_sessions[selected_session]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle text input
user_input = st.chat_input("Ask me anything...")
placeholder = st.empty()

# Upload widget inside the placeholder
uploaded_file = placeholder.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
st.write("\n" * 10)
if user_input:
    st.session_state.chat_sessions[st.session_state.current_session].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using Groq's LLM
    response = llm.invoke(user_input)  # Using llm.invoke directly for generating text-based response

    # Display AI response
    bot_reply = response.content
    st.session_state.chat_sessions[st.session_state.current_session].append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Upload image

if uploaded_file:
    # Save file locally
    image_path = "temp_image.jpg"
    
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64
    encoded_image = encode_image(image_path)

    # Static image-related prompt
    static_prompt = "Please analyze this image and provide insights based on the visible objects, colors, and any visible activity. Describe the image in detail."

    # Prepare the prompt for AI (including both image and the static prompt)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": static_prompt},  # Static prompt
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

# Add custom CSS for more aesthetics
st.markdown("""
    <style>
        .css-1aumxhk {
            padding: 10px;
            background-color: #f1f1f1;
        }
        .css-1uovwhk {
            border-radius: 10px;
            padding: 15px;
            background-color: #ffffff;
        }
        .css-ffhzg2 {
            padding: 20px;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)
