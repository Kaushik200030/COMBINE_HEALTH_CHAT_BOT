# Deployment Guide

This guide covers deploying the Insurance Policy Chatbot to various platforms.

## Prerequisites

- OpenAI API key
- Python 3.11+ or Docker
- Git (for version control)

## Deployment Options

### Option 1: Streamlit Community Cloud (Easiest)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app/ui/streamlit_app.py`
   - Add secrets:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `API_BASE_URL`: Your API endpoint (if separate)

3. **Deploy API Separately** (if needed)
   - Use Railway, Render, or Heroku for the FastAPI backend
   - Update `API_BASE_URL` in Streamlit secrets

### Option 2: Railway

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Create Railway Project**
   ```bash
   railway init
   railway up
   ```

3. **Set Environment Variables**
   ```bash
   railway variables set OPENAI_API_KEY=your_key
   ```

4. **Deploy**
   ```bash
   railway up
   ```

### Option 3: Render

1. **Create Web Service**
   - Go to https://render.com
   - Create new Web Service
   - Connect GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`

2. **Set Environment Variables**
   - `OPENAI_API_KEY`
   - `API_HOST=0.0.0.0`
   - `API_PORT=8000`

3. **Deploy Streamlit Separately**
   - Create another Web Service
   - Start command: `streamlit run app/ui/streamlit_app.py`

### Option 4: Docker Deployment

1. **Build Image**
   ```bash
   docker build -t insurance-chatbot .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Or Run Manually**
   ```bash
   docker run -d \
     -p 8000:8000 \
     -p 8501:8501 \
     -e OPENAI_API_KEY=your_key \
     -v $(pwd)/data:/app/data \
     insurance-chatbot
   ```

### Option 5: Local Deployment

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY=your_key
   ```

3. **Ingest Data**
   ```bash
   python scripts/ingest_data.py --limit 10
   ```

4. **Start Services**
   ```bash
   # Terminal 1: API
   python main.py
   
   # Terminal 2: Streamlit
   python run_streamlit.py
   ```

## Post-Deployment Checklist

- [ ] Verify API health endpoint: `GET /api/health`
- [ ] Test chat endpoint with sample query
- [ ] Verify vector database has loaded chunks
- [ ] Test Streamlit UI loads correctly
- [ ] Verify source citations work
- [ ] Check error handling for edge cases
- [ ] Monitor API usage and costs

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `API_BASE_URL`: API endpoint URL (default: http://localhost:8000)
- `VECTOR_DB_PATH`: Path to vector database (default: ./data/index/vector_db)
- `EMBEDDING_MODEL`: Embedding model (default: text-embedding-3-small)
- `CHAT_MODEL`: Chat model (default: gpt-4o-mini)
- `LOG_LEVEL`: Logging level (default: INFO)

## Data Ingestion

Before the chatbot can answer questions, you need to ingest policy data:

```bash
# Ingest policies (limit for testing)
python scripts/ingest_data.py --limit 10

# Or use API endpoint
curl -X POST "http://localhost:8000/api/ingest/start" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'
```

## Monitoring

- Check API logs for errors
- Monitor OpenAI API usage
- Track vector database size
- Monitor response times

## Troubleshooting

### API Not Responding
- Check if port 8000 is available
- Verify environment variables are set
- Check logs for errors

### No Results from Queries
- Verify vector database has data: `GET /api/ingest/status`
- Re-run data ingestion if needed
- Check embedding generation is working

### Streamlit Can't Connect to API
- Verify API_BASE_URL is correct
- Check API is running and accessible
- Verify CORS settings if needed
