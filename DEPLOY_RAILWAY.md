# Deploy to Railway (Free Tier Available)

Railway offers a free tier perfect for deploying both API and Streamlit.

## Prerequisites

1. GitHub account
2. Railway account (sign up at https://railway.app)

## Step 1: Prepare for Railway

### Create railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Create Procfile (for Heroku compatibility)

```
web: python main.py
```

## Step 2: Deploy API to Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect Python

### Configure Environment Variables

In Railway dashboard, add:
```
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**Note:** Railway doesn't support Ollama directly. You'll need to:
- Use Hugging Face instead, OR
- Deploy Ollama separately, OR
- Use template mode (no LLM)

### For Hugging Face (Recommended on Railway)

```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
```

## Step 3: Deploy Streamlit Separately

Create a second Railway service for Streamlit:

1. In same project, click "New Service"
2. Select "GitHub Repo" again
3. Set start command: `streamlit run app/ui/streamlit_app.py --server.port $PORT`
4. Add environment variable:
   ```
   API_BASE_URL=https://YOUR_API_URL.railway.app
   ```

## Step 4: Upload Data

You'll need to upload your vector database. Options:

1. **Include in repo** (not recommended for large files)
2. **Use Railway volumes** (persistent storage)
3. **Re-ingest on startup** (slower but works)

### Option: Re-ingest on Startup

Create `railway_startup.py`:
```python
"""Run on Railway startup to ensure data is loaded."""
from app.retrieval.vectordb import VectorDB
from pathlib import Path
import json

# Check if vector DB exists
db = VectorDB()
if not db.load_index():
    # Load from processed data if available
    processed_path = Path("data/processed/chunks.json")
    if processed_path.exists():
        with open(processed_path) as f:
            chunks = json.load(f)
        db.add_chunks(chunks)
        db.save_index()
```

## Railway Free Tier Limits

- $5 free credit per month
- 500 hours of usage
- Perfect for small projects!
