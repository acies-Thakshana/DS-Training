import streamlit as st
import os
from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from groq import Groq

# Set Groq API Key (Replace with your actual key)
GROQ_API_KEY = "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"

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Set up Streamlit UI
st.set_page_config(page_title="📄 Groq-Powered Document Q&A", layout="wide")
st.title("📄 Ask Questions from Any Document (Groq LLM)")
st.write("Upload a **.txt, .pdf, or .docx** file and ask questions based on its content.")

# File Upload
uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])

# Check if a file is uploaded
if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Define temp directory and file path
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"📂 File saved at: `{file_path}`")

    # Load the file based on its type
    if uploaded_file.name.endswith(".txt"):
        loader = TextLoader(file_path)
    elif uploaded_file.name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif uploaded_file.name.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        st.error("❌ Unsupported file type!")
        st.stop()

    # Load and process the document
    try:
        docs = loader.load()
        st.success("📑 Document processed successfully!")
    except Exception as e:
        st.error(f"❌ Error loading document: {str(e)}")
        st.stop()

    # Convert to embeddings & store in ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
    docs, 
    embeddings, 
    persist_directory="./chroma_db"  # Store vectors locally to prevent tenant issues
)

    vectorstore.persist()
    retriever = vectorstore.as_retriever()

    # User question input
    user_question = st.text_input("🧐 Ask a question about the document:")

    if user_question:
        with st.spinner("🔍 Searching document..."):
            # Retrieve relevant document chunks
            relevant_docs = retriever.get_relevant_documents(user_question)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # Call Groq API for response
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Groq model
                messages=[
                    {"role": "system", "content": "You are an AI that answers questions based on the given document."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_question}"}
                ]
            )

            # Display the AI-generated answer
            answer = response.choices[0].message.content
            st.subheader("🧠 AI Answer:")
            st.write(answer)
