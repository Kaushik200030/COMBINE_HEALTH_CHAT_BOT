# Cloud Deployment Configuration

## Why Ollama Won't Work on Cloud Platforms

**Ollama** requires:
- Local installation on the server
- Running as a separate service on port 11434
- Direct access to the machine

**Cloud platforms** (Railway, Render, Streamlit Cloud) don't allow:
- Installing system-level services like Ollama
- Running multiple services on the same container
- Accessing localhost services between containers

## Solution: Use Hugging Face Instead

Hugging Face models run **completely in Python** - no external services needed!

### How It Works

1. **Embeddings**: Already using sentence-transformers (works everywhere ✅)
2. **LLM**: Switch from Ollama to Hugging Face (works on cloud ✅)

### Configuration for Cloud

Set these environment variables in your cloud platform:

```bash
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

That's it! The app will automatically use Hugging Face instead of Ollama.

## How the Code Handles This

The `LLMService` class automatically detects the provider:

```python
if provider == "ollama":
    # Try Ollama (works locally)
elif provider == "huggingface":
    # Use Hugging Face (works everywhere)
else:
    # Fallback to template mode
```

## Testing Locally Before Deploying

You can test Hugging Face locally before deploying:

1. **Set environment variable:**
   ```bash
   export LLM_PROVIDER=huggingface
   export HF_MODEL=microsoft/Phi-3-mini-4k-instruct
   export HF_DEVICE=cpu
   ```

2. **Run the app:**
   ```bash
   python main.py
   ```

3. **First run will download the model** (~2-4GB, takes 5-10 minutes)
4. **Subsequent runs are instant** (model is cached)

## Model Options for Cloud

### Small & Fast (Recommended)
```bash
HF_MODEL=microsoft/Phi-3-mini-4k-instruct  # ~2GB
```

### Better Quality (Larger)
```bash
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.2  # ~7GB
```

### Very Small (Fastest)
```bash
HF_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0  # ~600MB
```

## Deployment Checklist

- [ ] Set `LLM_PROVIDER=huggingface` in cloud platform
- [ ] Set `HF_MODEL` (choose based on your needs)
- [ ] Set `HF_DEVICE=cpu` (cloud platforms usually don't have GPU)
- [ ] Ensure `requirements.txt` includes `transformers` and `torch`
- [ ] First deploy will take longer (model download)
- [ ] Test after deployment

## Performance Comparison

| Provider | Local | Cloud | Speed | Quality |
|----------|-------|-------|-------|---------|
| Ollama | ✅ Yes | ❌ No | Fast | Good |
| Hugging Face | ✅ Yes | ✅ Yes | Medium | Good |
| Template Mode | ✅ Yes | ✅ Yes | Fast | Basic |

## What Happens on First Deploy

1. Platform builds your app
2. Installs dependencies (including transformers)
3. Downloads Hugging Face model (5-10 minutes)
4. Caches model for future use
5. App is ready!

The model is cached, so subsequent deployments are faster.

## Troubleshooting

### Out of Memory Error
- Use smaller model: `microsoft/Phi-3-mini-4k-instruct`
- Or use `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

### Build Timeout
- Models download during build
- Increase build timeout in platform settings
- Or use smaller model

### Slow Responses
- Normal for CPU inference
- Consider upgrading to GPU plan (if available)
- Or use smaller, faster model
