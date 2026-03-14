# How Cloud Deployment Works (Without Ollama)

## The Problem with Ollama on Cloud

**Ollama** is a separate service that needs to:
- Run as a background process
- Listen on a port (11434)
- Be installed on the server

**Cloud platforms** (Railway, Render, Streamlit Cloud) run your code in isolated containers where:
- ❌ You can't install system services like Ollama
- ❌ You can't run multiple services easily
- ❌ Localhost connections between services don't work

## The Solution: Hugging Face

**Hugging Face** runs **entirely in Python** - no external services needed!

### How It Works

```
Your App (Python)
    │
    ├─→ Embeddings: sentence-transformers ✅ (already works)
    │
    └─→ LLM: Hugging Face Transformers ✅ (runs in same process)
```

Everything runs in **one Python process** - perfect for cloud!

## How the Code Handles This

The app is **already configured** to work both ways:

```python
# In app/services/llm_service.py
if provider == "ollama":
    # Use Ollama (for local development)
elif provider == "huggingface":
    # Use Hugging Face (for cloud deployment)
```

**You just set an environment variable** and it switches automatically!

## Deployment Steps

### 1. Set Environment Variable

In your cloud platform (Railway/Render/Streamlit Cloud), add:

```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
```

### 2. Deploy

That's it! The app will:
1. Detect `LLM_PROVIDER=huggingface`
2. Load Hugging Face model (downloads on first deploy)
3. Run everything in one process
4. Work perfectly on cloud!

## What Happens During Deployment

### First Deploy (5-10 minutes)
1. Platform installs Python dependencies
2. Downloads Hugging Face model (~2GB for Phi-3-mini)
3. Caches model for future use
4. App starts and works!

### Subsequent Deploys (2-3 minutes)
- Model is cached, so much faster
- Only code changes are deployed

## Comparison

| Feature | Ollama (Local) | Hugging Face (Cloud) |
|---------|----------------|---------------------|
| Works locally | ✅ Yes | ✅ Yes |
| Works on cloud | ❌ No | ✅ Yes |
| External service | ✅ Yes (separate) | ❌ No (in-process) |
| Setup complexity | Medium | Easy |
| Model download | Manual | Automatic |

## Testing Before Deploy

You can test Hugging Face locally:

```bash
# Set environment variable
export LLM_PROVIDER=huggingface

# Run the app
python main.py
```

First run downloads the model, then it works just like Ollama!

## Default Configuration

I've updated the default to `huggingface` so it works on cloud out of the box:

```python
# app/core/config.py
llm_provider: str = os.getenv("LLM_PROVIDER", "huggingface")  # Default to cloud-compatible
```

**For local with Ollama**, just set:
```bash
export LLM_PROVIDER=ollama
```

## Summary

✅ **Cloud deployment works because:**
1. Hugging Face runs in Python (no external services)
2. Code automatically detects the provider
3. Just set `LLM_PROVIDER=huggingface` environment variable
4. Everything else works the same!

✅ **You get the same functionality:**
- Same RAG system
- Same hybrid search
- Same source citations
- Same quality answers

The only difference is **which LLM backend** is used - but the user experience is identical!
