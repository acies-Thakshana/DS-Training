import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# API key for Groq
API_KEY = "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"

# Initialize Streamlit app
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Define the available models
MODELS = {
    "DEEPSEEK": "deepseek-r1-distill-qwen-32b",
    "LLMA": "llama-3.3-70b-versatile",
}

# Function to initialize Groq AI with the selected model
def get_groq_model(selected_model, api_key=API_KEY, temperature=0.7):
    return ChatGroq(
        groq_api_key=api_key,
        model_name=selected_model,
        temperature=temperature
    )

# Create a ChatPromptTemplate with system and user messages
def create_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant"),
        ("user", "{question}")
    ])

# Function to generate a response using Langchain + Groq model
def generate_text(question, llm, prompt):
    chain = prompt | llm
    return chain.invoke({"question": question})

# Streamlit UI setup
def main():
    st.title("AI Chatbot")
    st.sidebar.title("Settings")
    
    # Dropdown for model selection
    selected_model = st.sidebar.selectbox(
        "Choose a model",
        options=list(MODELS.keys()),
        index=0
    )
    
    # Temperature slider for controlling creativity
    temperature = st.sidebar.slider("Set Creativity (Temperature)", 0.0, 1.0, 0.7, 0.1)

    model_name = MODELS[selected_model]
    llm = get_groq_model(model_name, temperature=temperature)
    prompt = create_prompt()

    # Styling for Streamlit
    st.markdown("""
        <style>
            .stTextInput > div > div > input {
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
            .stTitle {
                color: #2e3b4e;
                font-family: 'Arial', sans-serif;
            }
            .stMarkdown {
                font-family: 'Arial', sans-serif;
                color: #2e3b4e;
            }
            .stTextInput label {
                color: #4CAF50;
            }
            .chat-container {
                max-width: 800px;
                margin: 0 auto;
            }
            .user-message {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 8px;
                margin: 5px 0;
                width: fit-content;
            }
            .ai-message {
                background-color: #f1f1f1;
                color: black;
                padding: 10px;
                border-radius: 8px;
                margin: 5px 0;
                width: fit-content;
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize chat history if not already done
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display chat history in a styled container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.history:
            if message['sender'] == "User":
                st.markdown(f'<div class="user-message">{message["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message">{message["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input box for the user to ask a question
    user_input = st.text_input("Ask a question:")

    # When the user presses "Send", generate the response
    if st.button("Send"):
        if user_input:
            # Add user question to chat history
            st.session_state.history.append({"sender": "User", "text": user_input})

            # Display loading message
            with st.spinner("Groq AI is thinking..."):
                # Generate the response using Groq AI and Langchain
                response = generate_text(user_input, llm, prompt)

                # Add AI response to chat history
                st.session_state.history.append({"sender": "Groq AI", "text": response.content})

                # Display the AI's response
                st.write("Groq AI Response:")
                st.write(response.content)

    # Button to clear chat history
    if st.sidebar.button("Clear Chat History"):
        st.session_state.history = []

# Run the Streamlit app
if __name__ == "__main__":
    main()
