"""
Semantic search functionality for retrieving relevant verses from the Bhagavad Gita.
"""

import numpy as np
import faiss
from typing import List, Dict, Any, Tuple
from .utils import build_citation


class GitaRetriever:
    """Handles semantic search over the Bhagavad Gita verses."""
    
    def __init__(self, index, docs: List[Dict[str, Any]], model):
        self.index = index
        self.docs = docs
        self.model = model
    
    def search(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """
        Search for the most relevant verses given a query.
        Searches the entire database and returns the best matches.
        
        Args:
            query: The search query
            k: Number of top results to return (if None, uses dynamic selection)
            
        Returns:
            List of dictionaries containing verse information and similarity scores
        """
        if not query.strip():
            return []
        
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        # Search the entire index (all verses)
        total_verses = self.index.ntotal
        scores, indices = self.index.search(query_embedding.astype('float32'), total_verses)
        
        # Filter and rank results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx == -1:  # Invalid index
                continue
                
            # Only include results with meaningful similarity (score > 0.1)
            if score < 0.1:
                continue
                
            doc = self.docs[idx]
            result = {
                'id': doc['id'],
                'chapter': doc['chapter'],
                'verse': doc['verse'],
                'text': doc['text'],
                'sanskrit': doc.get('sanskrit'),
                'score': float(score),
                'rank': i + 1
            }
            results.append(result)
        
        # If k is specified, limit results
        if k is not None:
            results = results[:k]
        
        return results
    
    def search_best_answer(self, query: str) -> Dict[str, Any]:
        """
        Search the entire database and find the best single answer.
        
        Args:
            query: The search query
            
        Returns:
            Dictionary with the best verse and additional context
        """
        if not query.strip():
            return None
        
        # Search all verses
        all_results = self.search(query, k=None)
        
        if not all_results:
            return None
        
        # Get the best match
        best_match = all_results[0]
        
        # Get additional context (top 3-5 relevant verses)
        context_verses = all_results[1:5] if len(all_results) > 1 else []
        
        return {
            'best_verse': best_match,
            'context_verses': context_verses,
            'total_matches': len(all_results),
            'confidence': best_match['score']
        }
    
    def get_verse_by_citation(self, chapter: int, verse: int) -> Dict[str, Any]:
        """
        Get a specific verse by chapter and verse number.
        
        Args:
            chapter: Chapter number (1-18)
            verse: Verse number
            
        Returns:
            Dictionary containing verse information, or None if not found
        """
        for doc in self.docs:
            if doc['chapter'] == chapter and doc['verse'] == verse:
                return {
                    'id': doc['id'],
                    'chapter': doc['chapter'],
                    'verse': doc['verse'],
                    'text': doc['text'],
                    'sanskrit': doc.get('sanskrit'),
                    'score': 1.0,  # Perfect match
                    'rank': 1
                }
        return None
    
    def format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results into a readable string.
        
        Args:
            results: List of search results
            
        Returns:
            Formatted string with citations and text
        """
        if not results:
            return "No relevant verses found."
        
        formatted_parts = []
        for result in results:
            citation = build_citation(result['chapter'], result['verse'])
            formatted_parts.append(f"{citation} {result['text']}")
        
        return "\n\n".join(formatted_parts)
    
    def get_context_for_generation(self, results: List[Dict[str, Any]], max_length: int = 2000) -> str:
        """
        Get a compact context block for the generator, respecting length limits.
        
        Args:
            results: List of search results
            max_length: Maximum length of the context
            
        Returns:
            Formatted context string
        """
        if not results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for result in results:
            citation = build_citation(result['chapter'], result['verse'])
            text = result['text']
            
            # Truncate text if needed
            if current_length + len(text) + len(citation) + 10 > max_length:
                remaining = max_length - current_length - len(citation) - 10
                if remaining > 100:  # Only include if we have meaningful space
                    text = text[:remaining] + "..."
                else:
                    break
            
            context_parts.append(f"{citation} {text}")
            current_length += len(text) + len(citation) + 10
        
        return "\n\n".join(context_parts)
    
    def validate_citations(self, citations: List[str]) -> List[Dict[str, Any]]:
        """
        Validate that citations exist in the dataset.
        
        Args:
            citations: List of citation strings in format [chapter.verse]
            
        Returns:
            List of dictionaries with validation results
        """
        validation_results = []
        
        for citation in citations:
            try:
                # Parse citation
                chapter_verse = citation.strip('[]')
                chapter, verse = map(int, chapter_verse.split('.'))
                
                # Check if verse exists
                verse_data = self.get_verse_by_citation(chapter, verse)
                
                validation_results.append({
                    'citation': citation,
                    'exists': verse_data is not None,
                    'verse_data': verse_data
                })
                
            except (ValueError, IndexError):
                validation_results.append({
                    'citation': citation,
                    'exists': False,
                    'verse_data': None
                })
        
        return validation_results
