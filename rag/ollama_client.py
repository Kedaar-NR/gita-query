"""
Ollama client for local LLM integration with the Bhagavad Gita chatbot.
"""

import requests
import json
from typing import Optional, Dict, Any


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the Gita chatbot."""
        return """You answer life skills questions using only the provided Bhagavad Gita passages.

Instructions:
- Write 3-6 sentences maximum
- Put citations like [chapter.verse] after supporting sentences
- If passages don't contain an answer, say so briefly and show 1-3 related verses
- Keep a respectful, neutral tone
- No medical or legal advice
- Never invent facts or verses not in the provided passages
- Always base your answer on the given verses only"""
    
    def generate_answer(self, query: str, context: str) -> Optional[str]:
        """
        Generate answer using Ollama API.
        
        Args:
            query: User's question
            context: Retrieved verses as context
            
        Returns:
            Generated answer or None if API call fails
        """
        try:
            # Build the full prompt
            prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 300
                }
            }
            
            # Make the API request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'response' in result:
                    return result['response'].strip()
            
        except requests.exceptions.RequestException as e:
            print(f"Ollama API error: {e}")
        except Exception as e:
            print(f"Error generating answer with Ollama: {e}")
        
        return None
    
    def test_connection(self) -> bool:
        """
        Test if Ollama is running and accessible.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """
        List available models in Ollama.
        
        Returns:
            List of available model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except:
            pass
        return []
    
    def set_model(self, model: str):
        """Set the model to use for generation."""
        self.model = model


def create_ollama_client(model: str = "llama2") -> OllamaClient:
    """
    Create and test an Ollama client.
    
    Args:
        model: Model name to use (default: llama2)
        
    Returns:
        OllamaClient instance or None if connection fails
    """
    client = OllamaClient(model=model)
    
    if client.test_connection():
        print(f"✅ Connected to Ollama with model: {model}")
        return client
    else:
        print("❌ Could not connect to Ollama. Make sure it's running on localhost:11434")
        return None
