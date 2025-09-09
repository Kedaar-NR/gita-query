"""
Supabase-based retriever for the Gita Query chatbot.
Replaces FAISS with Supabase vector search.
"""

import os
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

class SupabaseRetriever:
    """Retriever that uses Supabase for vector search instead of FAISS."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the Supabase retriever."""
        self.model = SentenceTransformer(model_name)
        self.supabase = self._init_supabase()
        self.embedding_dim = 384  # all-MiniLM-L6-v2 dimension
        
    def _init_supabase(self) -> Client:
        """Initialize Supabase client."""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        return create_client(url, key)
    
    def search(self, query: str, k: int = 5, threshold: float = 0.1) -> List[Dict[str, Any]]:
        """Search for similar verses using Supabase vector search."""
        try:
            # Encode query
            query_embedding = self.model.encode([query])[0]
            
            # Search in Supabase using vector similarity
            result = self.supabase.rpc(
                'match_verses',
                {
                    'query_embedding': query_embedding.tolist(),
                    'match_threshold': threshold,
                    'match_count': k
                }
            ).execute()
            
            if result.data:
                return result.data
            else:
                logger.warning("No results from Supabase search")
                return []
                
        except Exception as e:
            logger.error(f"Supabase search failed: {e}")
            return []
    
    def search_best_answer(self, query: str) -> Dict[str, Any]:
        """Search for the best answer with context verses."""
        try:
            # Encode query
            query_embedding = self.model.encode([query])[0]
            
            # Get best match
            result = self.supabase.rpc(
                'match_verses',
                {
                    'query_embedding': query_embedding.tolist(),
                    'match_threshold': 0.1,
                    'match_count': 10
                }
            ).execute()
            
            if result.data:
                best_verse = result.data[0]
                context_verses = result.data[1:4] if len(result.data) > 1 else []
                
                return {
                    'best_verse': best_verse,
                    'context_verses': context_verses,
                    'total_found': len(result.data)
                }
            else:
                return {
                    'best_verse': None,
                    'context_verses': [],
                    'total_found': 0
                }
                
        except Exception as e:
            logger.error(f"Supabase best answer search failed: {e}")
            return {
                'best_verse': None,
                'context_verses': [],
                'total_found': 0
            }
    
    def get_total_verses(self) -> int:
        """Get total number of verses in the database."""
        try:
            result = self.supabase.table('verse_embeddings').select('id', count='exact').execute()
            return result.count or 0
        except Exception as e:
            logger.error(f"Failed to get total verses: {e}")
            return 0
