"""
Answer generation for the Bhagavad Gita chatbot.
Supports both generative (with LLM) and extractive approaches.
"""

import os
import re
from typing import List, Dict, Any, Optional
from .utils import extract_citations_from_text, build_citation

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass


class GitaAnswerer:
    """Handles answer generation for life skills questions using Bhagavad Gita verses."""
    
    def __init__(self):
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for generative models."""
        return """You answer life skills questions using only the provided Bhagavad Gita passages.

Instructions:
- Write 3-6 sentences maximum
- Put citations like [chapter.verse] after supporting sentences
- If passages don't contain an answer, say so briefly and show 1-3 related verses
- Keep a respectful, neutral tone
- No medical or legal advice
- Never invent facts or verses not in the provided passages
- Always base your answer on the given verses only"""

    def generate_answer_gemini(self, query: str, context: str) -> Optional[str]:
        """
        Generate answer using Google's Gemini API.
        
        Args:
            query: User's question
            context: Retrieved verses as context
            
        Returns:
            Generated answer or None if API call fails
        """
        try:
            import google.generativeai as genai
            
            # Check for API key
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                return None
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Build prompt
            prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
            
            # Generate response
            response = model.generate_content(prompt)
            
            if response and response.candidates:
                # Access text content safely
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    text_content = candidate.content.parts[0].text
                    if text_content:
                        return text_content.strip()
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return None
        
        return None
    
    def generate_answer_openai(self, query: str, context: str) -> Optional[str]:
        """
        Generate answer using OpenAI's API.
        
        Args:
            query: User's question
            context: Retrieved verses as context
            
        Returns:
            Generated answer or None if API call fails
        """
        try:
            from openai import OpenAI
            
            # Check for API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return None
            
            # Initialize client
            client = OpenAI(api_key=api_key)
            
            # Build messages
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ]
            
            # Generate response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3,
                max_tokens=300
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
        
        return None
    
    def extractive_answer(self, query: str, passages: List[Dict[str, Any]]) -> str:
        """
        Create an intelligent extractive answer from the best passages.
        
        Args:
            query: User's question
            passages: List of retrieved passages
            
        Returns:
            Intelligent answer with the best verse and summary
        """
        if not passages:
            return "I couldn't find relevant verses in the Bhagavad Gita to answer your question."
        
        # Get the best match (highest score)
        best_passage = passages[0]
        best_citation = build_citation(best_passage['chapter'], best_passage['verse'])
        
        # Extract the core message from the best verse
        verse_text = best_passage['text']
        
        # Find the most relevant part of the verse
        query_words = set(query.lower().split())
        sentences = re.split(r'[.!?]+', verse_text)
        
        best_sentence = ""
        best_score = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            sentence_words = set(sentence.lower().split())
            score = len(query_words.intersection(sentence_words))
            
            if score > best_score:
                best_score = score
                best_sentence = sentence
        
        # If no good sentence found, use the beginning of the verse
        if not best_sentence:
            best_sentence = verse_text.split('.')[0] + "."
        
        # Create a concise, intelligent answer
        answer = f"The Bhagavad Gita teaches: {best_sentence} {best_citation}"
        
        # Add context if there are other relevant verses
        if len(passages) > 1:
            context_verses = passages[1:3]  # Take 2 more verses for context
            context_citations = [build_citation(p['chapter'], p['verse']) for p in context_verses]
            answer += f"\n\nRelated guidance: {', '.join(context_citations)}"
        
        return answer
    
    def generate_answer_ollama(self, query: str, context: str) -> Optional[str]:
        """
        Generate answer using Ollama API.
        
        Args:
            query: User's question
            context: Retrieved verses as context
            
        Returns:
            Generated answer or None if API call fails
        """
        try:
            from .ollama_client import OllamaClient
            
            # Create Ollama client
            client = OllamaClient()
            if not client.test_connection():
                return None
            
            return client.generate_answer(query, context)
            
        except Exception as e:
            print(f"Ollama integration error: {e}")
            return None

    def generate_answer(self, query: str, passages: List[Dict[str, Any]], model_type: str = "extractive") -> str:
        """
        Generate an answer using the specified method.
        
        Args:
            query: User's question
            passages: List of retrieved passages
            model_type: "gemini", "openai", "ollama", or "extractive"
            
        Returns:
            Generated answer
        """
        if not passages:
            return "I couldn't find relevant verses in the Bhagavad Gita to answer your question."
        
        # Prepare context
        context_parts = []
        for passage in passages:
            citation = build_citation(passage['chapter'], passage['verse'])
            context_parts.append(f"{citation} {passage['text']}")
        context = "\n\n".join(context_parts)
        
        # Try generative methods first if requested
        if model_type == "gemini":
            answer = self.generate_answer_gemini(query, context)
            if answer:
                return answer
        
        elif model_type == "openai":
            answer = self.generate_answer_openai(query, context)
            if answer:
                return answer
        
        elif model_type == "ollama":
            answer = self.generate_answer_ollama(query, context)
            if answer:
                return answer
        
        # Fallback to extractive
        return self.extractive_answer(query, passages)
    
    def validate_answer(self, answer: str, passages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate that the answer only uses citations from the provided passages.
        
        Args:
            answer: Generated answer
            passages: List of passages used to generate the answer
            
        Returns:
            Validation results
        """
        # Extract citations from answer
        answer_citations = set(extract_citations_from_text(answer))
        
        # Get citations from passages
        passage_citations = set()
        for passage in passages:
            citation = build_citation(passage['chapter'], passage['verse'])
            passage_citations.add(citation)
        
        # Check for invalid citations
        invalid_citations = answer_citations - passage_citations
        
        return {
            'valid': len(invalid_citations) == 0,
            'invalid_citations': list(invalid_citations),
            'answer_citations': list(answer_citations),
            'passage_citations': list(passage_citations)
        }
