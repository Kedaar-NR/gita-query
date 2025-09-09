"""
Ollama-based answerer for the Gita Query chatbot.
Uses local LLM via Ollama instead of cloud APIs.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import ollama

logger = logging.getLogger(__name__)

class OllamaAnswerer:
    """Answerer that uses Ollama for local LLM inference."""
    
    def __init__(self, model_name: str = "llama3.1:8b"):
        """Initialize the Ollama answerer."""
        self.model_name = model_name
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Test connection
        try:
            ollama.list()
            logger.info(f"Connected to Ollama at {self.base_url}")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}")
    
    def generate_answer(self, query: str, passages: List[Dict[str, Any]]) -> str:
        """Generate an answer using Ollama."""
        if not passages:
            return "I couldn't find relevant passages to answer your question."
        
        # Format context
        context = self._format_context(passages)
        
        # System prompt
        system_prompt = """You answer life skills questions using only the provided Bhagavad Gita passages. 
Write 3-6 sentences. Put citations like [chapter.verse] after supporting sentences. 
If passages don't contain an answer, say so briefly and show 1-3 related verses. 
Keep a respectful, neutral tone. No medical or legal advice."""
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {query}\n\nContext: {context}"}
                ]
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return self._fallback_answer(passages)
    
    def _format_context(self, passages: List[Dict[str, Any]]) -> str:
        """Format passages for the LLM."""
        context_parts = []
        for passage in passages:
            citation = f"[{passage['chapter']}.{passage['verse']}]"
            context_parts.append(f"{citation} {passage['text']}")
        return "\n\n".join(context_parts)
    
    def _fallback_answer(self, passages: List[Dict[str, Any]]) -> str:
        """Fallback answer when Ollama fails."""
        if not passages:
            return "I couldn't find relevant passages to answer your question."
        
        best_passage = passages[0]
        citation = f"[{best_passage['chapter']}.{best_passage['verse']}]"
        
        return f"Based on the Bhagavad Gita {citation}: {best_passage['text']}"
