# Gita Query - Ollama & Supabase Setup

This guide shows how to run the Gita Query chatbot using Ollama (local LLM) and Supabase (vector database) instead of Streamlit Cloud.

## Prerequisites

1. **Ollama** - Install from [ollama.ai](https://ollama.ai)
2. **Supabase Account** - Sign up at [supabase.com](https://supabase.com)
3. **Python 3.8+** - Make sure you have Python installed

## Setup Steps

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Start Ollama and Pull Model

```bash
# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull llama3.1:8b
# or
ollama pull mistral:7b
```

### 3. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > API
4. Copy your Project URL and anon key

### 4. Set Up Database Schema

1. In Supabase, go to SQL Editor
2. Run the SQL from `supabase_schema.sql`
3. This creates tables for verse embeddings and documents

### 5. Install Python Dependencies

```bash
pip install -r requirements_ollama.txt
```

### 6. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Supabase credentials
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

### 7. Populate Database

```bash
# Run the indexer to populate Supabase
python -c "
from rag.indexer import GitaIndexer
from rag.supabase_retriever import SupabaseRetriever

# Create indexer
indexer = GitaIndexer()

# Load and index data
indexer.load_dataset()
indexer.build_index()

# Save to Supabase (you'll need to implement this)
print('Indexing complete!')
"
```

### 8. Run the App

```bash
streamlit run app_ollama.py
```

## Benefits of This Setup

- **Privacy**: All data stays local (Ollama) or in your control (Supabase)
- **Cost**: No API costs for LLM inference
- **Performance**: Fast vector search with Supabase
- **Customization**: Full control over models and database

## Troubleshooting

### Ollama Issues
- Make sure Ollama is running: `ollama serve`
- Check available models: `ollama list`
- Test connection: `ollama run llama3.1:8b`

### Supabase Issues
- Verify your URL and key in `.env`
- Check if tables were created in SQL Editor
- Ensure vector extension is enabled

### Python Issues
- Make sure all dependencies are installed
- Check Python version (3.8+)
- Verify environment variables are set

## Alternative: Hybrid Setup

You can also use:
- **Supabase** for vector storage
- **OpenAI/Gemini** for LLM (instead of Ollama)
- **Streamlit** for UI

Just modify the environment variables and answerer configuration.
