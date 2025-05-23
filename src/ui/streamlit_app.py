import sys
import os

# Ensure the root of the project is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from src.utils.config_loader import load_config
from src.embeddings.embedder import embed_texts
from src.vector_store.pinecone_client import connect_pinecone_and_get_index
from src.chat.context_retriever import retrieve_context
from src.chat.prompt_builder import build_context_prompt
from src.chat.llm_interface import get_chat_model
from langchain_openai import OpenAIEmbeddings

# # Load API keys and configuration
cfg = load_config('config.yaml')

# # Initialize embedding model, vector store, and chat model
embedder = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=2048, openai_api_key=cfg["open_ai"])
index = connect_pinecone_and_get_index(cfg["pinecone"], cfg["pinecone_index"])
chat_model = get_chat_model(cfg["open_ai"])

# Streamlit UI setup
st.set_page_config(page_title="📊 Financial RAG Chatbot", layout="wide")
st.title("💬 Financial Analyst Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_query = st.chat_input("Ask a question about the financial Excel data...")

if user_query:
    with st.spinner("Retrieving relevant context and generating response..."):
        # Step 1: Retrieve context from Pinecone
        retrieved_chunks = retrieve_context(user_query, index, embedder)

        # Step 2: Build prompt for LLM using retrieved context
        final_prompt = build_context_prompt(user_query, retrieved_chunks)

        # Step 3: Call LLM with the prompt
        response = chat_model.invoke(final_prompt)

        # Step 4: Save to session history
        st.session_state.history.append({"user": user_query, "bot": response.content})

# Display conversation history
for message in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(message["user"])
    with st.chat_message("assistant"):
        st.markdown(message["bot"])
