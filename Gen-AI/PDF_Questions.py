import os
import streamlit as st
import fitz  # PyMuPDF for PDF reading
import faiss
import numpy as np

# LangChain imports
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up the Groq API key (Replace with your actual key)
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
  # Change model if needed
    temperature=0.7
)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text.strip()

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# Function to embed text into FAISS
def create_faiss_index(text_chunks):
    # Load embeddings model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Convert text chunks into embeddings
    embeddings = embedding_model.embed_documents(text_chunks)

    # Convert to numpy array
    embeddings_np = np.array(embeddings)

    # Create FAISS index
    dim = embeddings_np.shape[1]  # Dimensionality of the embeddings
    index = faiss.IndexFlatL2(dim)  # L2 (Euclidean distance) index
    index.add(embeddings_np)  # Add embeddings to the index

    return index, embedding_model

# Function to retrieve the top-k relevant chunks
def retrieve_top_k(query, text_chunks, index, embedding_model, k=5):
    query_embedding = np.array(embedding_model.embed_query(query)).reshape(1, -1)
    _, indices = index.search(query_embedding, k)
    return [text_chunks[i] for i in indices[0]]

# Streamlit UI
st.title("📄 Research Paper Q&A with AI")
st.write("Upload a **research paper (PDF)** and ask questions about its content.")

# File uploader for the PDF
uploaded_file = st.file_uploader("Upload your PDF here", type="pdf")

if uploaded_file:
    # Extract text from PDF
    paper_text = extract_text_from_pdf(uploaded_file)

    # Show extracted text summary
    st.subheader("📜 Extracted Text Summary:")
    st.write(paper_text[:1000] + " ...")  # Display only first 1000 characters

    # Split text into chunks
    text_chunks = split_text_into_chunks(paper_text)

    # Create FAISS index and embeddings
    index, embedding_model = create_faiss_index(text_chunks)

    # User asks a question
    query = st.text_input("🔍 Ask a question about the paper:")

    if query:
        # Retrieve relevant chunks
        relevant_chunks = retrieve_top_k(query, text_chunks, index, embedding_model, k=5)

        # # Display retrieved text chunks
        # st.subheader("📌 Relevant Sections from the Paper:")
        # for i, chunk in enumerate(relevant_chunks, start=1):
        #     st.markdown(f"**Chunk {i}:**")
        #     st.write(chunk)
        #     st.markdown("---")  # Separator

        # Use Groq LLM to generate an answer
        context = "\n".join(relevant_chunks)
        final_query = f"Based on the following text, answer: {query}\n\n{context}"

        # Get LLM response
        response = llm.invoke(final_query)
        response_text = response.content  # Extract clean text
        st.subheader("🤖 AI Answer:")
        st.write(response_text)

