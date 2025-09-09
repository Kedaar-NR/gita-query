"""
Streamlit chat interface for the Bhagavad Gita chatbot.
"""

import streamlit as st
import time
import os
from typing import List, Dict, Any
from rag import initialize_indexer, GitaRetriever, GitaAnswerer, safety_check, build_citation

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass


def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'indexer' not in st.session_state:
        st.session_state.indexer = None
    if 'retriever' not in st.session_state:
        st.session_state.retriever = None
    if 'answerer' not in st.session_state:
        st.session_state.answerer = None
    
    # Check for API keys (from environment or Streamlit secrets)
    try:
        google_key = os.getenv('GOOGLE_API_KEY') or st.secrets.get('GOOGLE_API_KEY', '')
        openai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    except:
        # Fallback if secrets are not available
        google_key = os.getenv('GOOGLE_API_KEY', '')
        openai_key = os.getenv('OPENAI_API_KEY', '')
    
    st.session_state.google_api_key_set = bool(google_key)
    st.session_state.openai_api_key_set = bool(openai_key)


def load_rag_components():
    """Load the RAG components (indexer, retriever, answerer)."""
    if st.session_state.indexer is None:
        with st.spinner("Loading Bhagavad Gita dataset and building search index..."):
            try:
                # Initialize indexer
                st.session_state.indexer = initialize_indexer()
                
                # Initialize retriever
                index = st.session_state.indexer.get_index()
                docs = st.session_state.indexer.get_docs()
                model = st.session_state.indexer.get_model()
                st.session_state.retriever = GitaRetriever(index, docs, model)
                
                # Initialize answerer
                st.session_state.answerer = GitaAnswerer()
                
                st.success("Dataset loaded successfully!")
                
            except Exception as e:
                st.error(f"Error loading dataset: {e}")
                st.stop()


def display_message(role: str, content: str, sources: List[Dict[str, Any]] = None):
    """Display a chat message with optional sources."""
    with st.chat_message(role):
        st.markdown(content)
        
        if sources and role == "assistant":
            with st.expander("Sources", expanded=False):
                for source in sources:
                    citation = build_citation(source['chapter'], source['verse'])
                    st.markdown(f"**{citation}**")
                    st.text(source['text'])
                    st.markdown("---")


def process_query(query: str, model_type: str, k: int) -> tuple[str, List[Dict[str, Any]]]:
    """
    Process a user query and return answer with sources.
    Searches the entire database for the best answer.
    
    Args:
        query: User's question
        model_type: Type of model to use ("extractive", "gemini", "openai")
        k: Number of passages to show in sources (not used for search)
        
    Returns:
        Tuple of (answer, sources)
    """
    # Safety check
    if not safety_check(query):
        return "I can help you with questions about life, spirituality, and personal growth based on the Bhagavad Gita.", []
    
    # Search the entire database for the best answer
    search_result = st.session_state.retriever.search_best_answer(query)
    
    if not search_result:
        return "I couldn't find relevant verses in the Bhagavad Gita to answer your question. Please try rephrasing your question or asking about topics like duty, focus, relationships, or personal growth.", []
    
    # Get the best verse and context
    best_verse = search_result['best_verse']
    context_verses = search_result['context_verses']
    
    # Combine best verse with context for answer generation
    all_passages = [best_verse] + context_verses
    
    # Generate answer using the best verse
    answer = st.session_state.answerer.generate_answer(query, [best_verse], model_type)
    
    # Return sources (limit to k for display)
    sources = all_passages[:k] if k else all_passages
    
    return answer, sources


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Bhagavad Gita Chatbot",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("Bhagavad Gita Chatbot")
    st.markdown("Ask life skills questions and get answers based on the wisdom of the Bhagavad Gita.")
    st.markdown("**Citations are shown in square brackets like [2.47]**")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Model selection
        model_options = {
            "No LLM (Extractive)": "extractive",
            "Gemini": "gemini", 
            "OpenAI": "openai"
        }
        
        selected_model = st.selectbox(
            "Answer Generation Method",
            options=list(model_options.keys()),
            index=0
        )
        model_type = model_options[selected_model]
        
        # Passages slider
        k = st.slider(
            "Number of verses to show in sources",
            min_value=3,
            max_value=10,
            value=5,
            help="The system searches the entire database and finds the best answer. This controls how many verses to show in the Sources section."
        )
        
        # API key info
        st.markdown("---")
        st.markdown("### API Keys (Optional)")
        
        if model_type == "gemini":
            if not st.session_state.get('google_api_key_set'):
                st.info("Set GOOGLE_API_KEY environment variable to use Gemini")
            else:
                st.success("Google API key found")
        
        elif model_type == "openai":
            if not st.session_state.get('openai_api_key_set'):
                st.info("Set OPENAI_API_KEY environment variable to use OpenAI")
            else:
                st.success("OpenAI API key found")
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Load RAG components
    load_rag_components()
    
    # Check API keys
    import os
    st.session_state.google_api_key_set = bool(os.getenv('GOOGLE_API_KEY'))
    st.session_state.openai_api_key_set = bool(os.getenv('OPENAI_API_KEY'))
    
    # Display chat messages
    for message in st.session_state.messages:
        display_message(
            message["role"], 
            message["content"], 
            message.get("sources", [])
        )
    
    # Chat input
    if prompt := st.chat_input("Ask about duty, focus, anxiety, relationships, or personal growth..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message("user", prompt)
        
        # Process query
        with st.chat_message("assistant"):
            with st.spinner("Searching the Bhagavad Gita..."):
                answer, sources = process_query(prompt, model_type, k)
            
            # Display answer
            st.markdown(answer)
            
            # Display sources
            if sources:
                with st.expander("Sources", expanded=False):
                    for source in sources:
                        citation = build_citation(source['chapter'], source['verse'])
                        st.markdown(f"**{citation}**")
                        st.text(source['text'])
                        st.markdown("---")
        
        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer,
            "sources": sources
        })
    


if __name__ == "__main__":
    main()
