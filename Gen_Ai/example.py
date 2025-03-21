import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Initialize Groq LLM
API_KEY = "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"

llm = ChatGroq(
    groq_api_key=API_KEY,
    model_name="llama-3.3-70b-versatile",  
    temperature=0.7
)

# Define the chat prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{question}")
])

def generate_text(question):
    """Generate response from Groq LLM."""
    chain = prompt | llm
    response = chain.invoke({"question": question})
    return response.content

# Streamlit UI Configuration
st.set_page_config(page_title="AI Chatbot", page_icon="☀️", layout="wide")


st.title("🤖 AI Chatbot with Groq & Streamlit")
st.write("Chat with an AI assistant ")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI response
    response = generate_text(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)