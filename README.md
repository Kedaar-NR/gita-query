# Bhagavad Gita Chatbot 
Explanations written by me, Kedaar, if you want to make your own chatbot with a completely different dataset.

A fully working chatbot that answers life skills questions using the wisdom of the Bhagavad Gita. The bot retrieves the most relevant verses and provides answers with clear citations.

**Dataset Source**: [JDhruv14/Bhagavad-Gita_Dataset](https://huggingface.co/datasets/JDhruv14/Bhagavad-Gita_Dataset) on Hugging Face

**Live Demo**: [Try the chatbot online](https://gita-query.streamlit.app) 

<img width="1443" height="1341" alt="image" src="https://github.com/user-attachments/assets/5a101c4c-1e64-4684-9f0c-2b00aa02ffe9" />


## Deployment Options

This chatbot can be deployed in multiple ways:

- **Streamlit Cloud** (Current): Easy deployment, free hosting - see `DEPLOYMENT.md`
- **Ollama + Supabase** (Recommended): Privacy-focused, no API costs - see `OLLAMA_SUPABASE_SETUP.md`
- **Hybrid Cloud**: Supabase + OpenAI/Gemini for best performance
- **Self-Hosted**: Complete control with Docker
- **Serverless**: Modern deployment with Vercel/Netlify

See `DEPLOYMENT_OPTIONS.md` for a complete comparison of all deployment methods.

## Quick Start

**Just want to run it? Here's how:**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the chatbot:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser to:** `http://localhost:8501`

4. **Ask questions like:**
   - "How do I stay focused?"
   - "How do I handle anxiety?"
   - "What should I do when facing difficult decisions?"

**That's it!** The chatbot will search through all 700 verses of the Bhagavad Gita and give you the best answer with proper citations.

## Features

- **Semantic Search**: Uses sentence transformers and FAISS for fast, accurate verse retrieval
- **Multiple Answer Methods**: Supports extractive answers (no API keys needed) and generative answers (Gemini/OpenAI)
- **Accurate Citations**: All answers include proper citations in format [chapter.verse]
- **Offline Operation**: Works completely offline after initial dataset download
- **Privacy-Focused**: No user queries are logged to external services
- **Streamlit UI**: Clean, responsive chat interface

## Complete Setup Guide (Step-by-Step)

This section explains exactly what to do and what each step means, including all the technical jargon.

### Step 1: Install Python Dependencies

**What you're doing**: Installing all the software libraries this chatbot needs to work.

```bash
pip install -r requirements.txt
```

**What this means**:
- `pip` = Python's package installer (like an app store for Python code)
- `requirements.txt` = A file listing all the libraries we need
- This downloads and installs: Streamlit (web interface), sentence-transformers (AI for understanding text), FAISS (fast search), and more

**What you'll see**: Lots of download progress bars. This is normal and takes 2-5 minutes.

### Step 2: Set Up API Keys (Optional but Recommended)

**What you're doing**: Getting access to AI services that can write more natural answers.

**Why it's optional**: The chatbot works without these, but answers will be more basic.

#### Option A: Google Gemini (Free, Recommended)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")

Then run this command in your terminal:
```bash
export GOOGLE_API_KEY="AIza_your_actual_key_here"
```

#### Option B: OpenAI (Paid, More Expensive)

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign up/login and create a new API key
3. Copy the key (starts with "sk-...")

Then run this command in your terminal:
```bash
export OPENAI_API_KEY="sk-your_actual_key_here"
```

**What these do**:
- **API Key** = A password that lets our app use Google's or OpenAI's AI services
- **Environment Variable** = A way to store the key securely on your computer
- **Generative AI** = AI that can write new text (vs just copying existing text)

### Step 3: Run the Chatbot

```bash
streamlit run app.py
```

**What happens**:
1. **First time only**: Downloads the Bhagavad Gita dataset (700 verses) from Hugging Face
2. **First time only**: Creates a search index (like a super-fast Google for the verses)
3. **Every time**: Opens your web browser to the chatbot interface

**What you'll see**:
- Terminal shows: "Building index..." (first time only, takes 30-60 seconds)
- Browser opens to: `http://localhost:8501`
- Chat interface appears with a text box

**If the browser doesn't open automatically**:
- Copy this URL: `http://localhost:8501`
- Paste it into your web browser
- The chatbot interface will load

**To stop the chatbot**:
- Press `Ctrl+C` in the terminal
- Or close the terminal window

### Step 4: Start Chatting!

**How to use**:
1. Type a question in the text box (e.g., "How do I handle stress?")
2. Press Enter or click Send
3. Get an answer with citations like [2.47]
4. Click "Sources" to see the exact verses used

**What the sidebar controls do**:
- **Answer Method**: Choose between basic answers (no API key needed) or AI-generated answers (needs API key)
- **Number of verses**: How many verses to search through (3-10, more = better context but longer answers)

## Technical Jargon Explained

### Core Concepts

**RAG (Retrieval-Augmented Generation)**:
- **Retrieval** = Finding relevant verses from the Bhagavad Gita
- **Augmented** = Enhanced with AI
- **Generation** = Creating new answers
- **In simple terms**: Find the right verses, then use AI to write a good answer based on them

**Semantic Search**:
- **Semantic** = Meaning-based (not just keyword matching)
- **Search** = Finding relevant information
- **In simple terms**: Understands what you're asking for, even if you use different words

**Embeddings**:
- **What it is**: Converting text into numbers that represent meaning
- **Why it matters**: Computers can't read text, but they can do math with numbers
- **Example**: "anxiety" and "worry" get similar number patterns, so the system knows they're related

**FAISS Index**:
- **FAISS** = Facebook AI Similarity Search (a fast search library)
- **Index** = A pre-built search structure (like a book's index, but for AI)
- **In simple terms**: A super-fast way to find the most relevant verses

### Answer Types

**Extractive Answers**:
- **What it is**: Taking sentences directly from the retrieved verses
- **Pros**: Always accurate, no API costs, works offline
- **Cons**: Can be choppy or repetitive

**Generative Answers**:
- **What it is**: AI writing new sentences based on the verses
- **Pros**: More natural, better flow, easier to read
- **Cons**: Requires API key, costs money, needs internet

### File Structure Explained

```
app.py                 # The main web interface (what you see in browser)
rag/                   # The "brain" of the chatbot
├── indexer.py         # Downloads data and builds search index
├── retriever.py       # Finds relevant verses for your questions
├── answer.py          # Creates answers (both types)
└── utils.py           # Helper functions (citations, safety checks)
eval/                  # Testing and quality assurance
└── eval.py           # Checks if answers are accurate
```

### Performance Metrics

**Cold Start (30-60 seconds)**:
- **What it is**: First time running the app
- **Why it takes time**: Downloading dataset + building search index
- **After first run**: Starts in 2-3 seconds

**Query Response (<1 second)**:
- **What it is**: Time to get an answer after you ask a question
- **Why it's fast**: Pre-built search index + efficient algorithms

**Memory Usage (~200MB)**:
- **What it is**: How much RAM the app uses
- **Why it matters**: More than this might slow down your computer

**Storage (~50MB)**:
- **What it is**: How much disk space the cached files take
- **What's cached**: Search index + processed verses for fast startup

## ⭐⭐⭐ How to Build Your Own Chatbot from Any Hugging Face Dataset (by Kedaar)

**Want to create a chatbot for your own dataset?** This section shows you exactly how to adapt this code for any text dataset on Hugging Face.

### Step-by-Step Process

#### **Step 1: Choose Your Dataset**

**Find a text dataset on Hugging Face:**
1. Go to [huggingface.co/datasets](https://huggingface.co/datasets)
2. Look for text-based datasets (not images/audio)
3. Good examples: `squad`, `wikitext`, `bookcorpus`, `philosophy_qa`

**What makes a good dataset:**
- ✅ Has text content (questions, answers, documents, books)
- ✅ Has 1000+ entries (more = better)
- ✅ Has clear field names (like 'question', 'answer', 'text')

#### **Step 2: Explore Your Dataset**

**Run this code to understand your dataset:**
```python
from datasets import load_dataset

# Replace with your dataset name
dataset = load_dataset("your_dataset_name")

# See the structure
print("Dataset info:", dataset)
print("First entry:", dataset['train'][0])
print("Column names:", dataset['train'].column_names)
```

**What you need to find:**
- What fields contain the text you want to search
- How many entries are there
- What the data looks like

#### **Step 3: Copy This Project**

**Simple approach:**
1. Copy this entire folder
2. Rename it to your project name
3. You now have all the code structure

#### **Step 4: Modify 3 Key Files**

**File 1: `rag/indexer.py` (Line 25)**
```python
# CHANGE THIS LINE:
dataset = load_dataset("JDhruv14/Bhagavad-Gita_Dataset")

# TO THIS:
dataset = load_dataset("your_dataset_name")
```

**File 2: `rag/utils.py` (Lines 15-25)**
```python
# UPDATE THE FIELD MAPPINGS:
field_mappings = {
    'chapter': ['chapter', 'Chapter', 'ch'],           # Your ID field
    'verse': ['verse', 'Verse', 'v'],                  # Your ID field  
    'sanskrit': ['sanskrit', 'Sanskrit', 'sa'],        # Optional
    'hindi': ['hindi', 'Hindi', 'hi'],                 # Optional
    'english': ['english', 'English', 'en', 'text', 'content', 'answer']  # Your main text
}
```

**File 3: `app.py` (Lines 105-106)**
```python
# CHANGE THE TITLE:
st.title("🕉️ Your Custom Chatbot")
st.markdown("Ask questions and get answers based on your dataset.")
```

#### **Step 5: Test Your Changes**

**Run this to test:**
```bash
python quick_test.py
```

**If it works, you'll see:**
- Dataset loading successfully
- Index being built
- Test questions working

#### **Step 6: Customize Further (Optional)**

**Change the citation format in `rag/utils.py`:**
```python
def build_citation(chapter: int, verse: int) -> str:
    # Instead of [2.47], you might want [ID_123] or [Page_45]
    return f"[{chapter}.{verse}]"  # Change this line
```

**Change the answer style in `rag/answer.py`:**
```python
# Line 157 - change how answers are formatted
answer = f"The Bhagavad Gita teaches: {best_sentence} {best_citation}"
# Change to: f"Based on your dataset: {best_sentence} {best_citation}"
```

### Real Example: Philosophy Q&A Chatbot

**Let's say you want to use the `philosophy_qa` dataset:**

**Step 1: Change dataset name**
```python
# In rag/indexer.py, line 25:
dataset = load_dataset("philosophy_qa")
```

**Step 2: Update field mappings**
```python
# In rag/utils.py:
field_mappings = {
    'question': ['question', 'q', 'query'],
    'answer': ['answer', 'a', 'response'], 
    'text': ['answer'],  # Use answer as main text
    'id': ['id', 'ID', 'index']
}
```

**Step 3: Update text extraction**
```python
# In rag/indexer.py, around line 54:
# Instead of verses, create Q&A format
question = normalized.get('question', '')
answer = normalized.get('answer', '')
canonical_text = f"Q: {question}\nA: {answer}"
```

**Step 4: Update citations**
```python
# In rag/utils.py:
def build_citation(entry_id: str) -> str:
    return f"[{entry_id}]"  # Use ID instead of chapter.verse
```

**Step 5: Test it**
```bash
python quick_test.py
```

### Common Issues & Solutions

**Issue: "No verses loaded"**
- **Solution**: Check your field mappings in `rag/utils.py`
- **Debug**: Run `python debug_dataset.py` to see your data structure

**Issue: "Import errors"**
- **Solution**: Make sure you're in the right directory and run `pip install -r requirements.txt`

**Issue: "Search results are bad"**
- **Solution**: Try a different sentence transformer model in `rag/indexer.py` line 15

**Issue: "Answers are too long"**
- **Solution**: Modify the text extraction in `rag/indexer.py` to use shorter text

### Performance Tips

**For large datasets (10,000+ entries):**
- The system will work but might be slower
- Consider using a smaller subset for testing

**For small datasets (<100 entries):**
- Still works, but answers might be limited
- Consider combining multiple small datasets

**For faster startup:**
- The index is cached after first run
- Subsequent runs will be much faster

### You're Done!

**Your custom chatbot is ready!**

1. **Run it**: `streamlit run app.py`
2. **Open browser**: `http://localhost:8501`
3. **Ask questions** about your dataset
4. **Get answers** with proper citations

**The system will:**
- ✅ Search through your entire dataset
- ✅ Find the most relevant content
- ✅ Provide answers with citations
- ✅ Work offline after first download

## Usage

1. **Ask Life Skills Questions**: Focus on topics like duty, focus, anxiety, relationships, or personal growth
2. **Get Grounded Answers**: All answers come directly from Bhagavad Gita verses
3. **Check Sources**: Expand the "Sources" section to see the exact verses used
4. **Adjust Settings**: Use the sidebar to change the number of verses retrieved or switch between answer methods

### Example Questions

- "How do I focus on duty without worrying about results?"
- "How do I handle anxiety before exams?"
- "What should I do when facing difficult decisions?"
- "How can I find peace in stressful situations?"

## Architecture

```
app.py                 # Streamlit chat interface
rag/
├── indexer.py         # Dataset loading and FAISS index creation
├── retriever.py       # Semantic search functionality
├── answer.py          # Answer generation (generative + extractive)
└── utils.py           # Schema helpers and citation formatting
```

## Dataset

Uses the [JDhruv14/Bhagavad-Gita_Dataset](https://huggingface.co/datasets/JDhruv14/Bhagavad-Gita_Dataset) from Hugging Face, containing:
- 700 verses from all 18 chapters
- Sanskrit original text
- Hindi and English translations
- Proper verse numbering and citations

## Answer Methods

### 1. Extractive (Default)
- No API keys required
- Concise answers from top retrieved verses
- Always includes proper citations
- Works completely offline

### 2. Generative (Optional)
- Uses Gemini or OpenAI for more natural responses
- Still grounded in retrieved verses only
- Maintains citation accuracy
- Requires API keys

## Quality Assurance

- **Citation Validation**: All citations are verified against the dataset
- **Safety Checks**: Prevents medical/legal advice requests
- **Schema Normalization**: Handles dataset field variations
- **Error Handling**: Graceful fallbacks for API failures

## Performance

- **Cold Start**: ~30 seconds for initial index building
- **Query Response**: <1 second for typical laptop
- **Memory Usage**: ~200MB for full dataset and index
- **Storage**: ~50MB for cached index and documents

## Development

### Running Tests

```bash
python -m pytest eval/
```

### Evaluation Script

```bash
python eval/eval.py
```

## Troubleshooting

### Common Issues

1. **"Port 8501 is already in use"**
   - **Solution**: Stop the previous Streamlit app with `Ctrl+C` or run: `pkill -f streamlit`

2. **"Dataset Download Fails"**
   - **Solution**: Ensure internet connection and Hugging Face access

3. **"Import errors"**
   - **Solution**: Run `pip install -r requirements.txt`
   - **IDE import errors**: These are IDE configuration issues, not code problems. Run `python check_environment.py` to verify packages are installed correctly. again

4. **"Slow Performance"**
   - **Solution**: Ensure sufficient RAM (4GB+ recommended)

5. **"Browser doesn't open automatically"**
   - **Solution**: Manually open `http://localhost:8501` in your browser

### Reset Index

If you encounter issues, delete these files to rebuild the index:
- `gita.faiss`
- `gita_docs.pkl`

### Test the Installation

Run this to verify everything works:
```bash
python quick_test.py
```

### Get Help

If you're still having issues:
1. Check that Python 3.9+ is installed
2. Make sure you're in the correct directory
3. Try running `python test_installation.py` to check dependencies

## License

This project is for educational and spiritual purposes. The Bhagavad Gita dataset is used under appropriate licensing terms.

## Contributing

Contributions are welcome! Please focus on:
- Improving answer quality
- Adding new evaluation metrics
- Enhancing the user interface
- Optimizing performance

