# 🚂 Railway Deployment Guide

Railway is perfect for deploying your chatbot - better control, no Python version issues!

## ✅ Why Railway?

- ✅ Full control over Python version (3.11)
- ✅ Supports all dependencies (FAISS, lxml, etc.)
- ✅ Can run both API and Streamlit in same project
- ✅ Free tier: $5 credit/month
- ✅ No cold starts
- ✅ Persistent storage available

## 📋 Step-by-Step Deployment

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Sign up with GitHub (easiest)
3. Authorize Railway to access your repos

### Step 2: Deploy API Service

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `Kaushik200030/COMBINE_HEALTH_CHAT_BOT`
4. Railway will auto-detect Python and start building

### Step 3: Configure API Service

1. Click on your service
2. Go to **"Variables"** tab
3. Add these environment variables:

```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
EMBEDDING_MODEL=all-MiniLM-L6-v2
API_HOST=0.0.0.0
API_PORT=$PORT
```

**Note:** Railway automatically sets `$PORT` - your code already handles this!

### Step 4: Deploy Streamlit UI (Separate Service)

1. In the same project, click **"New Service"**
2. Select **"GitHub Repo"** again
3. Choose the same repository
4. Go to **"Settings"** → **"Deploy"**
5. Set **Start Command:**
   ```
   streamlit run app/ui/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
   ```

### Step 5: Configure Streamlit Service

1. Go to **"Variables"** tab
2. Add:
   ```
   API_BASE_URL=https://YOUR_API_SERVICE.railway.app
   ```
   (Replace with your actual API URL from Railway)

### Step 6: Handle Data Files

Your vector database is already in git (`data/index/vector_db/`), so it will be available!

**Option A: Use Existing Data (Recommended)**
- Data files are already in your repo
- They'll be available on Railway automatically
- No additional setup needed!

**Option B: Re-ingest on First Deploy**
- If data isn't loading, the app will use processed chunks
- Or create a startup script (see below)

## 🔧 Railway-Specific Configuration

### Port Configuration

Railway sets `$PORT` automatically. Your `main.py` already handles this correctly!

### Python Version

Railway uses Python 3.11 by default (perfect for your dependencies).

### Build Settings

Railway will:
1. Install dependencies from `requirements.txt`
2. Run `python main.py` (from railway.json)
3. Expose on port from `$PORT`

## 📝 Environment Variables Summary

### API Service:
```
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu
EMBEDDING_MODEL=all-MiniLM-L6-v2
API_HOST=0.0.0.0
API_PORT=$PORT
```

### Streamlit Service:
```
API_BASE_URL=https://your-api-service.railway.app
```

## 🚀 After Deployment

1. **Get your URLs:**
   - API: `https://your-api-service.railway.app`
   - Streamlit: `https://your-streamlit-service.railway.app`

2. **Test the API:**
   ```bash
   curl https://your-api-service.railway.app/api/health
   ```

3. **Access Streamlit UI:**
   - Open the Streamlit URL in your browser
   - Start asking questions!

## 💰 Railway Free Tier

- **$5 free credit/month**
- **500 hours of usage**
- Perfect for your chatbot!

## 🆘 Troubleshooting

### Build Fails
- Check Railway logs
- Ensure all dependencies are in `requirements.txt`
- Python 3.11 is used automatically

### API Not Responding
- Check `API_PORT=$PORT` is set
- Verify service is running (green status)

### Streamlit Can't Connect to API
- Check `API_BASE_URL` is correct
- Use the Railway-provided URL (not localhost)

### Data Not Loading
- Data files are in git, should work automatically
- Check logs for vector DB loading messages

## 📚 Next Steps

1. Deploy API service
2. Get API URL
3. Deploy Streamlit service with API URL
4. Test both services
5. Share your chatbot URL!

Your chatbot will be live at: `https://your-streamlit-service.railway.app` 🎉
