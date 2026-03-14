# Deploy to Render (Free Tier)

Render offers free hosting for both web services and static sites.

## Prerequisites

1. GitHub account
2. Render account (sign up at https://render.com)

## Step 1: Deploy API to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `insurance-chatbot-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free

### Environment Variables

Add in Render dashboard:
```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
EMBEDDING_MODEL=all-MiniLM-L6-v2
PYTHON_VERSION=3.11
```

## Step 2: Deploy Streamlit to Render

1. Click "New +" → "Web Service" again
2. Same repository
3. Configure:
   - **Name**: `insurance-chatbot-ui`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app/ui/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - **Plan**: Free

### Environment Variables

```
API_BASE_URL=https://insurance-chatbot-api.onrender.com
STREAMLIT_SERVER_PORT=10000
```

## Step 3: Upload Data Files

### Option A: Include in Git (Small datasets)

```bash
# Add data files to git
git add data/
git commit -m "Add data files"
git push
```

### Option B: Use Render Disk (Persistent Storage)

1. In Render dashboard, go to your service
2. Click "Disk" tab
3. Mount disk at `/opt/render/project/src/data`
4. Upload your `data/` folder contents

### Option C: Re-ingest on First Deploy

Modify your startup to check and ingest if needed.

## Render Free Tier

- 750 hours/month free
- Spins down after 15 min inactivity
- First request after spin-down takes ~30 seconds

## Important Notes

1. **Ollama won't work on Render** - Use Hugging Face instead
2. **First deploy takes time** - Models download on first run
3. **Cold starts** - Free tier has cold starts after inactivity
