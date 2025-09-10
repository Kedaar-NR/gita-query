"""
Simple test script to verify the installation works correctly.
"""

import sys
import os

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import streamlit
        print("streamlit")
    except ImportError as e:
        print(f"streamlit: {e}")
        return False
    
    try:
        import datasets
        print("datasets")
    except ImportError as e:
        print(f"datasets: {e}")
        return False
    
    try:
        import sentence_transformers
        print("sentence-transformers")
    except ImportError as e:
        print(f"sentence-transformers: {e}")
        return False
    
    try:
        import faiss
        print("faiss-cpu")
    except ImportError as e:
        print(f"faiss-cpu: {e}")
        return False
    
    try:
        import numpy
        print("numpy")
    except ImportError as e:
        print(f"numpy: {e}")
        return False
    
    try:
        import pandas
        print("pandas")
    except ImportError as e:
        print(f"pandas: {e}")
        return False
    
    # Test optional imports
    try:
        import google.generativeai
        print("google-generativeai (optional)")
    except ImportError:
        print("google-generativeai (optional, not installed)")
    
    try:
        import openai
        print("openai (optional)")
    except ImportError:
        print("openai (optional, not installed)")
    
    return True


def test_rag_components():
    """Test that RAG components can be imported."""
    print("\nTesting RAG components...")
    
    try:
        from rag import GitaIndexer, GitaRetriever, GitaAnswerer
        print("RAG components imported successfully")
        return True
    except ImportError as e:
        print(f"RAG components: {e}")
        return False


def main():
    """Run all tests."""
    print("Bhagavad Gita Chatbot - Installation Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test RAG components
    rag_ok = test_rag_components()
    
    print("\n" + "=" * 50)
    if imports_ok and rag_ok:
        print("All tests passed! Installation is working correctly.")
        print("\nNext steps:")
        print("1. Run: streamlit run app.py")
        print("2. Optional: Set GOOGLE_API_KEY or OPENAI_API_KEY environment variables")
        return True
    else:
        print("Some tests failed. Please check the installation.")
        print("\nTry running: pip install -r requirements.txt")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
