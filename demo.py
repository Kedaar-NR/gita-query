"""
Demo script showing how the Bhagavad Gita chatbot works.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag import initialize_indexer, GitaRetriever, GitaAnswerer


def demo_chatbot():
    """Demonstrate the chatbot functionality."""
    print("🕉️ Bhagavad Gita Chatbot Demo")
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
        print("✅ Components loaded successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Demo questions
    demo_questions = [
        "How do I focus on duty without worrying about results?",
        "How do I handle anxiety before exams?",
        "What should I do when facing difficult decisions?",
        "How can I find peace in stressful situations?"
    ]
    
    print(f"\nDataset loaded: {len(docs)} verses from the Bhagavad Gita")
    print(f"Search index: {index.ntotal} vectors")
    
    print("\n" + "=" * 50)
    print("DEMO CONVERSATIONS")
    print("=" * 50)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n🤔 Question {i}: {question}")
        print("-" * 40)
        
        # Retrieve relevant passages
        passages = retriever.search(question, k=3)
        print(f"Found {len(passages)} relevant verses:")
        
        for passage in passages:
            citation = f"[{passage['chapter']}.{passage['verse']}]"
            print(f"  {citation} (score: {passage['score']:.3f})")
        
        # Generate answer
        answer = answerer.generate_answer(question, passages, "extractive")
        print(f"\n💭 Answer: {answer}")
        
        # Show sources
        print(f"\n📚 Sources:")
        for passage in passages:
            citation = f"[{passage['chapter']}.{passage['verse']}]"
            print(f"  {citation}: {passage['text'][:100]}...")
        
        print("\n" + "-" * 40)
    
    print("\n✅ Demo completed!")
    print("\nTo run the full chatbot:")
    print("streamlit run app.py")


if __name__ == "__main__":
    demo_chatbot()
