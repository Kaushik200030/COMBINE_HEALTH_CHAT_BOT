# Free Setup Guide - No API Keys Required! 🎉

This chatbot uses **100% free, open-source components**. No OpenAI API keys or paid services needed!

## Free Components Used

✅ **Python** - Free  
✅ **sentence-transformers** - Free embeddings (local)  
✅ **Ollama** - Free LLM (local, recommended)  
✅ **Hugging Face Transformers** - Alternative free LLM (local)  
✅ **FAISS** - Free vector database (open-source)  
✅ **BeautifulSoup** - Free web scraping  
✅ **Streamlit** - Free UI framework  
✅ **Streamlit Cloud** - Free deployment  

## Quick Setup

### Option 1: Ollama (Recommended - Easiest)

1. **Install Ollama**
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Or download from https://ollama.ai
   ```

2. **Download a model**
   ```bash
   ollama pull llama3.2
   # Or try: ollama pull mistral
   # Or try: ollama pull phi3
   ```

3. **Start Ollama** (it runs in the background)
   ```bash
   ollama serve
   ```

4. **Configure the app**
   ```bash
   # In .env file (or environment variables)
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

5. **Run the app**
   ```bash
   python main.py  # API
   python run_streamlit.py  # UI
   ```

### Option 2: Hugging Face Transformers (Completely Local)

1. **Install dependencies**
   ```bash
   pip install transformers torch accelerate
   ```

2. **Configure the app**
   ```bash
   # In .env file
   LLM_PROVIDER=huggingface
   HF_MODEL=microsoft/Phi-3-mini-4k-instruct
   HF_DEVICE=cpu  # or "cuda" if you have GPU
   ```

3. **Run the app**
   ```bash
   python main.py  # API
   python run_streamlit.py  # UI
   ```

**Note:** First run will download the model (~2-4GB). Subsequent runs are instant.

## Embeddings (Already Free!)

The app uses **sentence-transformers** which is completely free and runs locally:

- **Default model**: `all-MiniLM-L6-v2` (384 dimensions, ~80MB)
- **Better quality**: `all-mpnet-base-v2` (768 dimensions, ~420MB)

Change in `.env`:
```bash
EMBEDDING_MODEL=all-mpnet-base-v2
```

## No LLM? Use Template Mode

If you don't set up Ollama or Hugging Face, the app will use a simple template-based response system. It will still:
- ✅ Retrieve relevant policy chunks
- ✅ Show source citations
- ✅ Display policy information

Just won't have AI-generated answers (but you'll still get the relevant policy text).

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Embeddings (sentence-transformers) | $0 (local) |
| LLM (Ollama) | $0 (local) |
| Vector DB (FAISS) | $0 (open-source) |
| Web Scraping | $0 (local) |
| Streamlit UI | $0 (free tier) |
| Deployment (Streamlit Cloud) | $0 (free) |
| **TOTAL** | **$0** 🎉 |

## Troubleshooting

### Ollama not connecting?
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Hugging Face model too slow?
- Use a smaller model: `microsoft/Phi-3-mini-4k-instruct`
- Or use Ollama instead (faster)

### Out of memory?
- Use CPU mode: `HF_DEVICE=cpu`
- Use smaller embedding model: `all-MiniLM-L6-v2`
- Use smaller LLM model

## Recommended Models

### For Embeddings
- **Fast & Small**: `all-MiniLM-L6-v2` (384 dim, 80MB)
- **Better Quality**: `all-mpnet-base-v2` (768 dim, 420MB)

### For LLM (Ollama)
- **Fast & Good**: `llama3.2` (2B params)
- **Better Quality**: `mistral` (7B params)
- **Small & Fast**: `phi3` (3.8B params)

### For LLM (Hugging Face)
- **Small**: `microsoft/Phi-3-mini-4k-instruct` (3.8B)
- **Medium**: `mistralai/Mistral-7B-Instruct-v0.2` (7B)
- **Large**: `meta-llama/Llama-2-7b-chat-hf` (7B, requires approval)

## Next Steps

1. Choose your LLM provider (Ollama recommended)
2. Install and configure it
3. Run the ingestion script to load policies
4. Start the app and test!

Enjoy your completely free chatbot! 🚀
