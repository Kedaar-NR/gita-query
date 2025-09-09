"""
Streamlit app for Gita Query chatbot using Ollama and Supabase.
"""

import streamlit as st
import os
from rag.supabase_retriever import SupabaseRetriever
from rag.ollama_answerer import OllamaAnswerer
from rag.utils import build_citation, validate_verse_data

# Page config
st.set_page_config(
    page_title="Gita Query - Ollama & Supabase",
    page_icon="📖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "answerer" not in st.session_state:
    st.session_state.answerer = None

@st.cache_resource
def load_retriever():
    """Load the Supabase retriever."""
    try:
        return SupabaseRetriever()
    except Exception as e:
        st.error(f"Failed to load retriever: {e}")
        return None

@st.cache_resource
def load_answerer():
    """Load the Ollama answerer."""
    try:
        return OllamaAnswerer()
    except Exception as e:
        st.error(f"Failed to load answerer: {e}")
        return None

def main():
    """Main app function."""
    st.title("Gita Query - Ollama & Supabase")
    st.caption("Ask life skills questions and get answers from the Bhagavad Gita")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Model selection
        model_type = st.selectbox(
            "Answering Method",
            ["Ollama (Local LLM)", "Extractive Only"],
            help="Ollama uses a local language model, Extractive only uses retrieved text"
        )
        
        # Verses to show
        num_verses = st.slider(
            "Number of verses to show in sources",
            min_value=3,
            max_value=10,
            value=5,
            help="Number of verses to display in the sources section"
        )
        
        # Environment status
        st.subheader("Environment Status")
        
        # Check Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if supabase_url and supabase_key:
            st.success("✅ Supabase configured")
        else:
            st.error("❌ Supabase not configured")
            st.info("Set SUPABASE_URL and SUPABASE_KEY environment variables")
        
        # Check Ollama
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        if model_type == "Ollama (Local LLM)":
            st.info(f"Using Ollama model: {ollama_model}")
    
    # Load components
    if st.session_state.retriever is None:
        st.session_state.retriever = load_retriever()
    
    if st.session_state.answerer is None and model_type == "Ollama (Local LLM)":
        st.session_state.answerer = load_answerer()
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about life skills..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process query
        with st.chat_message("assistant"):
            with st.spinner("Searching the Bhagavad Gita..."):
                try:
                    # Search for relevant verses
                    if st.session_state.retriever:
                        results = st.session_state.retriever.search_best_answer(prompt)
                        
                        if results['best_verse']:
                            # Generate answer
                            if model_type == "Ollama (Local LLM)" and st.session_state.answerer:
                                answer = st.session_state.answerer.generate_answer(
                                    prompt, 
                                    [results['best_verse']] + results['context_verses']
                                )
                            else:
                                # Extractive answer
                                best_verse = results['best_verse']
                                citation = build_citation(best_verse['chapter'], best_verse['verse'])
                                answer = f"Based on the Bhagavad Gita {citation}: {best_verse['text']}"
                            
                            # Display answer
                            st.markdown(answer)
                            
                            # Show sources
                            with st.expander("Sources", expanded=False):
                                all_verses = [results['best_verse']] + results['context_verses']
                                for i, verse in enumerate(all_verses[:num_verses]):
                                    citation = build_citation(verse['chapter'], verse['verse'])
                                    st.markdown(f"**{citation}**")
                                    st.markdown(verse['text'])
                                    if i < len(all_verses) - 1:
                                        st.markdown("---")
                            
                            # Add assistant message
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        else:
                            st.error("I couldn't find relevant passages to answer your question.")
                            st.session_state.messages.append({"role": "assistant", "content": "I couldn't find relevant passages to answer your question."})
                    else:
                        st.error("Retriever not available. Please check your Supabase configuration.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {e}"})

if __name__ == "__main__":
    main()
