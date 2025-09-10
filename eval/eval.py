"""
Evaluation script for the Bhagavad Gita chatbot.
Tests answer quality and citation accuracy.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag import initialize_indexer, GitaRetriever, GitaAnswerer, build_citation, extract_citations_from_text


def test_questions():
    """Test questions with expected citations."""
    return [
        {
            "question": "How do I focus on duty without worrying about results?",
            "expected_citations": ["[2.47]", "[2.48]", "[2.49]"],
            "description": "Should cite the famous karma yoga verses"
        },
        {
            "question": "How do I handle anxiety and stress?",
            "expected_citations": ["[2.14]", "[2.15]", "[2.16]"],
            "description": "Should cite verses about equanimity and detachment"
        },
        {
            "question": "What should I do when facing difficult decisions?",
            "expected_citations": ["[2.31]", "[2.32]", "[2.33]"],
            "description": "Should cite verses about righteous action"
        },
        {
            "question": "How can I find peace in life?",
            "expected_citations": ["[2.70]", "[2.71]", "[2.72]"],
            "description": "Should cite verses about inner peace"
        },
        {
            "question": "How do I deal with failure and setbacks?",
            "expected_citations": ["[2.11]", "[2.12]", "[2.13]"],
            "description": "Should cite verses about impermanence and detachment"
        }
    ]


def validate_citations(answer: str, expected_citations: list) -> dict:
    """
    Validate that the answer contains expected citations.
    
    Args:
        answer: Generated answer
        expected_citations: List of expected citation strings
        
    Returns:
        Validation results
    """
    found_citations = extract_citations_from_text(answer)
    
    # Check for expected citations
    found_expected = [c for c in expected_citations if c in found_citations]
    
    # Check for unexpected citations
    unexpected = [c for c in found_citations if c not in expected_citations]
    
    return {
        "found_citations": found_citations,
        "expected_citations": expected_citations,
        "found_expected": found_expected,
        "unexpected": unexpected,
        "coverage": len(found_expected) / len(expected_citations) if expected_citations else 0
    }


def test_verse_existence(retriever: GitaRetriever, citations: list) -> dict:
    """
    Test that cited verses actually exist in the dataset.
    
    Args:
        retriever: GitaRetriever instance
        citations: List of citation strings
        
    Returns:
        Validation results
    """
    results = {}
    
    for citation in citations:
        try:
            # Parse citation
            chapter_verse = citation.strip('[]')
            chapter, verse = map(int, chapter_verse.split('.'))
            
            # Check if verse exists
            verse_data = retriever.get_verse_by_citation(chapter, verse)
            results[citation] = {
                "exists": verse_data is not None,
                "verse_data": verse_data
            }
            
        except (ValueError, IndexError):
            results[citation] = {
                "exists": False,
                "verse_data": None,
                "error": "Invalid citation format"
            }
    
    return results


def run_evaluation():
    """Run the complete evaluation suite."""
    print("🕉️ Bhagavad Gita Chatbot Evaluation")
    print("=" * 50)
    
    # Initialize components
    print("Loading RAG components...")
    try:
        indexer = initialize_indexer()
        index = indexer.get_index()
        docs = indexer.get_docs()
        model = indexer.get_model()
        retriever = GitaRetriever(index, docs, model)
        answerer = GitaAnswerer()
        print("✅ Components loaded successfully")
    except Exception as e:
        print(f"❌ Error loading components: {e}")
        return
    
    # Test questions
    test_cases = test_questions()
    
    print(f"\nRunning {len(test_cases)} test cases...")
    print("-" * 50)
    
    total_score = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['question']}")
        print(f"Description: {test_case['description']}")
        
        # Generate answer
        passages = retriever.search(test_case['question'], k=5)
        answer = answerer.generate_answer(test_case['question'], passages, "extractive")
        
        print(f"Answer: {answer}")
        
        # Validate citations
        citation_validation = validate_citations(answer, test_case['expected_citations'])
        
        print(f"Found citations: {citation_validation['found_citations']}")
        print(f"Expected citations: {citation_validation['expected_citations']}")
        print(f"Coverage: {citation_validation['coverage']:.2%}")
        
        # Test verse existence
        if citation_validation['found_citations']:
            existence_validation = test_verse_existence(retriever, citation_validation['found_citations'])
            
            invalid_verses = [c for c, result in existence_validation.items() if not result['exists']]
            if invalid_verses:
                print(f"❌ Invalid citations found: {invalid_verses}")
            else:
                print("✅ All citations are valid")
        
        # Calculate score
        score = citation_validation['coverage']
        total_score += score
        
        print(f"Score: {score:.2%}")
    
    # Final results
    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)
    
    average_score = total_score / total_tests
    print(f"Average Citation Coverage: {average_score:.2%}")
    
    if average_score >= 0.8:
        print("✅ Excellent performance!")
    elif average_score >= 0.6:
        print("⚠️ Good performance, room for improvement")
    else:
        print("❌ Poor performance, needs improvement")
    
    # Dataset statistics
    print(f"\nDataset Statistics:")
    print(f"Total verses: {len(docs)}")
    print(f"Index size: {index.ntotal} vectors")
    
    # Test specific verses
    print(f"\nTesting specific verses:")
    test_verses = ["[2.47]", "[2.48]", "[1.1]", "[18.78]"]
    for verse in test_verses:
        existence = test_verse_existence(retriever, [verse])
        status = "✅" if existence[verse]['exists'] else "❌"
        print(f"{status} {verse}: {'Found' if existence[verse]['exists'] else 'Not found'}")


if __name__ == "__main__":
    run_evaluation()
