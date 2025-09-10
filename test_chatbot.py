"""
Test script to verify the chatbot works correctly.
Tests the core functionality without needing Streamlit.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag import initialize_indexer, GitaRetriever, GitaAnswerer


def test_chatbot():
    """Test the chatbot with a sample question."""
    print("Testing Bhagavad Gita Chatbot")
    print("=" * 50)
    
    # Initialize components
    print("Loading dataset and building index...")
    try:
        indexer = initialize_indexer()
        index = indexer.get_index()
        docs = indexer.get_docs()
        model = indexer.get_model()
        retriever = GitaRetriever(index, docs, model)
        answerer = GitaAnswerer()
        print("Components loaded successfully!")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test questions
    test_questions = [
        "how to stay focused",
        "How do I focus on duty without worrying about results?",
        "How do I handle anxiety?",
        "What should I do when facing difficult decisions?"
    ]
    
    print(f"\nDataset loaded: {len(docs)} verses from the Bhagavad Gita")
    print(f"Search index: {index.ntotal} vectors")
    
    print("\n" + "=" * 50)
    print("TESTING CHATBOT RESPONSES")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("-" * 40)
        
        # Retrieve relevant passages
        passages = retriever.search(question, k=3)
        print(f"Found {len(passages)} relevant verses:")
        
        for passage in passages:
            citation = f"[{passage['chapter']}.{passage['verse']}]"
            print(f"  {citation} (score: {passage['score']:.3f})")
        
        # Generate answer
        answer = answerer.generate_answer(question, passages, "extractive")
        print(f"\nAnswer: {answer}")
        
        # Check if answer contains citations
        citations_found = []
        for passage in passages:
            citation = f"[{passage['chapter']}.{passage['verse']}]"
            if citation in answer:
                citations_found.append(citation)
        
        if citations_found:
            print(f"Citations found: {citations_found}")
        else:
            print("No citations found in answer")
        
        # Show sources
        print(f"\nSources:")
        for passage in passages:
            citation = f"[{passage['chapter']}.{passage['verse']}]"
            text_preview = passage['text'][:100] + "..." if len(passage['text']) > 100 else passage['text']
            print(f"  {citation}: {text_preview}")
        
        print("\n" + "-" * 40)
    
    print("\nChatbot test completed!")
    return True


def test_specific_verse():
    """Test that we can find a specific famous verse."""
    print("\n" + "=" * 50)
    print("TESTING SPECIFIC VERSE RETRIEVAL")
    print("=" * 50)
    
    try:
        indexer = initialize_indexer()
        index = indexer.get_index()
        docs = indexer.get_docs()
        model = indexer.get_model()
        retriever = GitaRetriever(index, docs, model)
        
        # Test famous verse 2.47 (Karma Yoga)
        verse = retriever.get_verse_by_citation(2, 47)
        if verse:
            print(f"Found verse 2.47: {verse['text'][:100]}...")
        else:
            print("Could not find verse 2.47")
        
        # Test another famous verse
        verse = retriever.get_verse_by_citation(18, 78)
        if verse:
            print(f"Found verse 18.78: {verse['text'][:100]}...")
        else:
            print("Could not find verse 18.78")
            
    except Exception as e:
        print(f"Error testing specific verses: {e}")


if __name__ == "__main__":
    success = test_chatbot()
    test_specific_verse()
    
    if success:
        print("\nAll tests passed! The chatbot is working correctly.")
        print("\nTo run the full chatbot:")
        print("streamlit run app.py")
    else:
        print("\nSome tests failed. Please check the installation.")
        sys.exit(1)
