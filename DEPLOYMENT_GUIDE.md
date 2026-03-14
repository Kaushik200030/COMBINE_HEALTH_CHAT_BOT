# Complete Deployment Guide

This guide covers all deployment options for your Insurance Policy Chatbot.

## 🚀 Quick Start - Choose Your Platform

### Option 1: Streamlit Cloud (Easiest) ⭐ Recommended
- **Free**: Yes
- **Difficulty**: ⭐ Easy
- **Best for**: Quick demo, personal projects
- **See**: [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)

### Option 2: Railway (Best Free Tier)
- **Free**: $5 credit/month
- **Difficulty**: ⭐⭐ Medium
- **Best for**: Production apps, better performance
- **See**: [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)

### Option 3: Render (Good Free Tier)
- **Free**: 750 hours/month
- **Difficulty**: ⭐⭐ Medium
- **Best for**: Reliable hosting, good documentation
- **See**: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] Code is pushed to GitHub
- [ ] `.env` file is NOT in git (use platform secrets instead)
- [ ] `requirements.txt` is up to date
- [ ] Data files are handled (see below)
- [ ] LLM provider is configured (Ollama won't work on most cloud platforms)

## 🔧 Data Files Handling

Your chatbot needs:
- Vector database (`data/index/vector_db/`)
- Processed chunks (`data/processed/chunks.json`)

### Option A: Include in Git (Small datasets < 100MB)
```bash
git add data/
git commit -m "Add data files"
```

### Option B: Re-ingest on Deploy
Create a startup script that ingests data if not present.

### Option C: External Storage
Use cloud storage (S3, etc.) and download on startup.

## 🤖 LLM Configuration for Cloud

**Important**: Ollama won't work on most cloud platforms. Use:

### Hugging Face (Recommended for Cloud)
```bash
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
```

### Or Template Mode (No LLM)
```bash
LLM_PROVIDER=none
# App will use template responses
```

## 📝 Environment Variables

Set these in your platform's dashboard:

### Required
```
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
```

### Optional
```
API_BASE_URL=https://your-api-url.com
VECTOR_DB_PATH=./data/index/vector_db
LOG_LEVEL=INFO
```

## 🐳 Docker Deployment

If you prefer Docker:

```bash
# Build
docker build -t insurance-chatbot .

# Run
docker run -p 8000:8000 -p 8501:8501 \
  -e LLM_PROVIDER=huggingface \
  -e HF_MODEL=microsoft/Phi-3-mini-4k-instruct \
  insurance-chatbot
```

## 🔍 Testing After Deployment

1. Check health endpoint: `https://your-api-url.com/api/health`
2. Test a query via API
3. Test Streamlit UI
4. Verify sources are displayed correctly

## 🆘 Troubleshooting

### Issue: Models not downloading
- **Solution**: Increase build timeout or use smaller models

### Issue: Out of memory
- **Solution**: Use smaller models or upgrade plan

### Issue: Cold starts too slow
- **Solution**: Use Railway (no cold starts) or upgrade Render plan

### Issue: API timeout
- **Solution**: Increase timeout in Streamlit app

## 📊 Platform Comparison

| Platform | Free Tier | Cold Starts | Best For |
|----------|-----------|-------------|----------|
| Streamlit Cloud | ✅ Unlimited | ❌ No | Quick demos |
| Railway | ✅ $5/month | ❌ No | Production |
| Render | ✅ 750 hrs | ⚠️ Yes (15 min) | Budget hosting |
| Heroku | ⚠️ Limited | ⚠️ Yes | Legacy apps |

## 🎯 Recommended Setup

For best results:
1. **API**: Deploy to Railway (no cold starts)
2. **UI**: Deploy to Streamlit Cloud (easiest)
3. **LLM**: Use Hugging Face (works everywhere)
4. **Data**: Include in repo or use persistent storage

## 📚 Next Steps

1. Choose your platform
2. Follow the specific deployment guide
3. Set environment variables
4. Deploy and test!

Need help? Check the specific deployment guides for detailed instructions.
