"""
Data loading and FAISS index creation for the Bhagavad Gita chatbot.
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Any
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import faiss
from .utils import normalize_schema, validate_verse_data, create_verse_id, clean_text


class GitaIndexer:
    """Handles loading the Bhagavad Gita dataset and creating a FAISS index."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.index = None
        self.docs = []
        self.index_file = "gita.faiss"
        self.docs_file = "gita_docs.pkl"
    
    def load_dataset(self) -> List[Dict[str, Any]]:
        """
        Load the Bhagavad Gita dataset from Hugging Face.
        Returns a list of normalized verse dictionaries.
        """
        print("Loading Bhagavad Gita dataset...")
        
        try:
            # Load the dataset
            dataset = load_dataset("JDhruv14/Bhagavad-Gita_Dataset")
            
            # Get the train split (which contains all verses)
            data = dataset['train']
            
            verses = []
            for row in data:
                # Normalize the schema to handle field name variations
                normalized = normalize_schema(row)
                
                # Validate the data (check for required fields)
                if not normalized.get('chapter') or not normalized.get('verse'):
                    continue
                
                # Check that we have either english or hindi text
                if not normalized.get('english') and not normalized.get('hindi'):
                    continue
                
                # Create canonical text format
                chapter = int(normalized['chapter'])
                verse_num = int(normalized['verse'])
                
                # Use English translation as primary text, fallback to Hindi
                text = normalized.get('english', normalized.get('hindi', ''))
                text = clean_text(text)
                
                if not text:
                    continue
                
                # Build canonical text
                sanskrit = normalized.get('sanskrit', '')
                if sanskrit:
                    sanskrit = clean_text(sanskrit)
                    canonical_text = f"Chapter {chapter}, Verse {verse_num}\n{sanskrit}\n\n{text}"
                else:
                    canonical_text = f"Chapter {chapter}, Verse {verse_num}\n\n{text}"
                
                verse_data = {
                    'id': create_verse_id(chapter, verse_num),
                    'chapter': chapter,
                    'verse': verse_num,
                    'text': canonical_text,
                    'sanskrit': sanskrit if sanskrit else None
                }
                
                verses.append(verse_data)
            
            print(f"Loaded {len(verses)} verses from the dataset")
            return verses
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            raise
    
    def create_embeddings(self, verses: List[Dict[str, Any]]) -> np.ndarray:
        """
        Create embeddings for all verses using sentence transformers.
        """
        print("Creating embeddings...")
        
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        
        # Extract texts for embedding
        texts = [verse['text'] for verse in verses]
        
        # Create embeddings
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        print(f"Created embeddings with shape: {embeddings.shape}")
        return embeddings
    
    def build_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        Build a FAISS index for fast similarity search.
        """
        print("Building FAISS index...")
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index (inner product for cosine similarity)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        
        # Add embeddings to index
        index.add(embeddings.astype('float32'))
        
        print(f"Built FAISS index with {index.ntotal} vectors")
        return index
    
    def save_index(self, index: faiss.Index, docs: List[Dict[str, Any]]):
        """
        Save the FAISS index and documents to disk.
        """
        print("Saving index and documents...")
        
        # Save FAISS index
        faiss.write_index(index, self.index_file)
        
        # Save documents
        with open(self.docs_file, 'wb') as f:
            pickle.dump(docs, f)
        
        print(f"Saved index to {self.index_file} and docs to {self.docs_file}")
    
    def load_index(self) -> bool:
        """
        Load the FAISS index and documents from disk.
        Returns True if successful, False otherwise.
        """
        if not os.path.exists(self.index_file) or not os.path.exists(self.docs_file):
            return False
        
        try:
            print("Loading existing index and documents...")
            
            # Load FAISS index
            self.index = faiss.read_index(self.index_file)
            
            # Load documents
            with open(self.docs_file, 'rb') as f:
                self.docs = pickle.load(f)
            
            # Load the sentence transformer model
            self.model = SentenceTransformer(self.model_name)
            
            print(f"Loaded index with {self.index.ntotal} vectors and {len(self.docs)} documents")
            return True
            
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def build_index(self) -> bool:
        """
        Build the complete index from scratch.
        Returns True if successful, False otherwise.
        """
        try:
            # Load dataset
            verses = self.load_dataset()
            if not verses:
                return False
            
            # Create embeddings
            embeddings = self.create_embeddings(verses)
            
            # Build FAISS index
            self.index = self.build_faiss_index(embeddings)
            
            # Store documents
            self.docs = verses
            
            # Save to disk
            self.save_index(self.index, self.docs)
            
            return True
            
        except Exception as e:
            print(f"Error building index: {e}")
            return False
    
    def get_index(self) -> faiss.Index:
        """Get the FAISS index."""
        return self.index
    
    def get_docs(self) -> List[Dict[str, Any]]:
        """Get the documents list."""
        return self.docs
    
    def get_model(self) -> SentenceTransformer:
        """Get the sentence transformer model."""
        return self.model


def initialize_indexer() -> GitaIndexer:
    """
    Initialize the indexer, loading from disk if available, otherwise building from scratch.
    """
    indexer = GitaIndexer()
    
    # Try to load existing index first
    if not indexer.load_index():
        print("No existing index found. Building new index...")
        if not indexer.build_index():
            raise RuntimeError("Failed to build index")
    
    return indexer
