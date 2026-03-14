# 🚀 Quick Deployment Guide

**Fastest way to deploy your chatbot!**

## Step 1: Push to GitHub

```bash
# Make sure you're in the project directory
cd "/Users/kaushikpattanayak/Desktop/Kaushik Work/COMBINE_HEALTH_CHAT_BOT"

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Insurance Policy Chatbot - Ready for deployment"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Choose Your Platform

### 🎯 Easiest: Streamlit Cloud (Recommended for Demo)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app/ui/streamlit_app.py`
6. Click "Deploy"

**Done!** Your app will be live at `https://YOUR_APP_NAME.streamlit.app`

**Note:** For Streamlit Cloud, you'll need to either:
- Deploy API separately (Railway/Render), OR
- Modify app to run everything internally (see below)

### 🚂 Best Performance: Railway

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python

**Set Environment Variables:**
```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**Done!** Your API will be live at `https://YOUR_APP.railway.app`

### 🎨 Good Alternative: Render

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Use the `render.yaml` file (already created!)

**Done!** Both API and UI will deploy automatically.

## Step 3: Configure Environment Variables

### For Hugging Face (Works on All Platforms)

Set these in your platform's dashboard:

```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### For Streamlit Cloud (If Using Separate API)

```
API_BASE_URL=https://your-api-url.railway.app
```

## Step 4: Handle Data Files

Your vector database needs to be available. Options:

### Option A: Include in Git (Recommended for Small Datasets)

```bash
# The .gitignore is already configured to allow data/processed/ and data/index/
git add data/processed/ data/index/
git commit -m "Add vector database"
git push
```

### Option B: Re-ingest on First Deploy

The app will automatically ingest data if the vector DB doesn't exist (slower first startup).

## 🎉 You're Done!

Your chatbot should now be live! Test it by:
1. Visiting your deployed URL
2. Asking a question like "What does the spinal pain ablation policy say?"
3. Checking that sources are displayed

## 📚 Need More Details?

- **Streamlit Cloud**: See [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)
- **Railway**: See [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)
- **Render**: See [DEPLOY_RENDER.md](DEPLOY_RENDER.md)
- **Complete Guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## ⚠️ Important Notes

1. **Ollama won't work on cloud platforms** - Use Hugging Face instead
2. **First deploy takes time** - Models download on first run (5-10 minutes)
3. **Free tiers have limits** - Monitor your usage
4. **Data files** - Make sure vector DB is included or will be re-ingested

## 🆘 Troubleshooting

**Issue**: Models not downloading
- **Fix**: Increase build timeout or use smaller models

**Issue**: Out of memory
- **Fix**: Use smaller models (Phi-3-mini) or upgrade plan

**Issue**: API timeout
- **Fix**: Already fixed in code (120s timeout)

**Issue**: Data not loading
- **Fix**: Include data files in git or use persistent storage
