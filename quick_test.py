"""
Quick test to verify the chatbot works with your specific question.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag import initialize_indexer, GitaRetriever, GitaAnswerer


def test_focus_question():
    """Test the specific question about staying focused."""
    print("Testing: 'how to stay focused'")
    print("=" * 50)
    
    # Initialize components
    print("Loading components...")
    indexer = initialize_indexer()
    index = indexer.get_index()
    docs = indexer.get_docs()
    model = indexer.get_model()
    retriever = GitaRetriever(index, docs, model)
    answerer = GitaAnswerer()
    
    # Test the specific question
    query = "how to stay focused"
    print(f"\n🤔 Question: {query}")
    
    # Search for the best answer
    search_result = retriever.search_best_answer(query)
    
    if search_result:
        best_verse = search_result['best_verse']
        context_verses = search_result['context_verses']
        
        print(f"\nFound {search_result['total_matches']} relevant verses")
        print(f"Confidence: {search_result['confidence']:.3f}")
        
        # Generate answer
        answer = answerer.generate_answer(query, [best_verse], "extractive")
        
        print(f"\nAnswer:")
        print(answer)
        
        print(f"\nBest verse: [{best_verse['chapter']}.{best_verse['verse']}]")
        print(f"Text: {best_verse['text'][:200]}...")
        
        if context_verses:
            print(f"\nRelated verses:")
            for verse in context_verses:
                print(f"  [{verse['chapter']}.{verse['verse']}] (score: {verse['score']:.3f})")
        
        print("\nTest completed successfully!")
        return True
    else:
        print("No relevant verses found")
        return False


if __name__ == "__main__":
    success = test_focus_question()
    if success:
        print("\nThe chatbot is working perfectly!")
        print("You can now run: streamlit run app.py")
    else:
        print("\nThere was an issue with the chatbot")
        sys.exit(1)
