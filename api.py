"""
FastAPI backend for the Bhagavad Gita chatbot.
Provides REST API endpoints for chat functionality.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from rag import initialize_indexer, GitaRetriever, GitaAnswerer, safety_check, build_citation


# Pydantic models
class ChatRequest(BaseModel):
    query: str
    model_type: str = "extractive"  # "extractive", "gemini", "openai", "ollama"
    k: int = 5  # Number of verses to show in sources


class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    model_used: str


class HealthResponse(BaseModel):
    status: str
    index_loaded: bool
    models_available: Dict[str, bool]


# Initialize FastAPI app
app = FastAPI(
    title="Bhagavad Gita Chatbot API",
    description="REST API for querying the Bhagavad Gita with RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for RAG components
indexer = None
retriever = None
answerer = None


@app.on_event("startup")
async def startup_event():
    """Initialize RAG components on startup."""
    global indexer, retriever, answerer
    
    try:
        # Initialize indexer
        indexer = initialize_indexer()
        
        # Initialize retriever
        index = indexer.get_index()
        docs = indexer.get_docs()
        model = indexer.get_model()
        retriever = GitaRetriever(index, docs, model)
        
        # Initialize answerer
        answerer = GitaAnswerer()
        
        print("✅ RAG components initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing RAG components: {e}")
        raise


@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    global indexer, retriever, answerer
    
    # Check if components are loaded
    index_loaded = all([indexer, retriever, answerer])
    
    # Check model availability
    models_available = {
        "extractive": True,  # Always available
        "gemini": False,
        "openai": False,
        "ollama": False
    }
    
    # Check API keys and Ollama
    import os
    models_available["gemini"] = bool(os.getenv('GOOGLE_API_KEY'))
    models_available["openai"] = bool(os.getenv('OPENAI_API_KEY'))
    
    # Check Ollama connection
    try:
        from rag.ollama_client import OllamaClient
        client = OllamaClient()
        models_available["ollama"] = client.test_connection()
    except:
        pass
    
    return HealthResponse(
        status="healthy" if index_loaded else "initializing",
        index_loaded=index_loaded,
        models_available=models_available
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat query and return answer with sources."""
    global retriever, answerer
    
    if not retriever or not answerer:
        raise HTTPException(status_code=503, detail="RAG components not initialized")
    
    # Safety check
    if not safety_check(request.query):
        return ChatResponse(
            answer="I can help you with questions about life, spirituality, and personal growth based on the Bhagavad Gita.",
            sources=[],
            model_used="safety_filter"
        )
    
    # Search for relevant verses
    search_result = retriever.search_best_answer(request.query)
    
    if not search_result:
        return ChatResponse(
            answer="I couldn't find relevant verses in the Bhagavad Gita to answer your question. Please try rephrasing your question or asking about topics like duty, focus, relationships, or personal growth.",
            sources=[],
            model_used=request.model_type
        )
    
    # Get the best verse and context
    best_verse = search_result['best_verse']
    context_verses = search_result['context_verses']
    
    # Combine best verse with context for answer generation
    all_passages = [best_verse] + context_verses
    
    # Generate answer
    answer = answerer.generate_answer(request.query, [best_verse], request.model_type)
    
    # Return sources (limit to k for display)
    sources = all_passages[:request.k] if request.k else all_passages
    
    return ChatResponse(
        answer=answer,
        sources=sources,
        model_used=request.model_type
    )


@app.get("/search")
async def search_verses(query: str, k: int = 10):
    """Search for verses without generating an answer."""
    global retriever
    
    if not retriever:
        raise HTTPException(status_code=503, detail="RAG components not initialized")
    
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    results = retriever.search(query, k=k)
    return {"query": query, "results": results}


@app.get("/verse/{chapter}/{verse}")
async def get_verse(chapter: int, verse: int):
    """Get a specific verse by chapter and verse number."""
    global retriever
    
    if not retriever:
        raise HTTPException(status_code=503, detail="RAG components not initialized")
    
    if not (1 <= chapter <= 18):
        raise HTTPException(status_code=400, detail="Chapter must be between 1 and 18")
    
    verse_data = retriever.get_verse_by_citation(chapter, verse)
    
    if not verse_data:
        raise HTTPException(status_code=404, detail=f"Verse {chapter}.{verse} not found")
    
    return verse_data


@app.get("/models")
async def list_available_models():
    """List available models and their status."""
    models = {
        "extractive": {"available": True, "description": "Extractive answers from verses"},
        "gemini": {"available": False, "description": "Google Gemini API"},
        "openai": {"available": False, "description": "OpenAI GPT API"},
        "ollama": {"available": False, "description": "Local Ollama models"}
    }
    
    # Check API keys
    import os
    models["gemini"]["available"] = bool(os.getenv('GOOGLE_API_KEY'))
    models["openai"]["available"] = bool(os.getenv('OPENAI_API_KEY'))
    
    # Check Ollama
    try:
        from rag.ollama_client import OllamaClient
        client = OllamaClient()
        models["ollama"]["available"] = client.test_connection()
        if models["ollama"]["available"]:
            models["ollama"]["installed_models"] = client.list_models()
    except:
        pass
    
    return models


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
