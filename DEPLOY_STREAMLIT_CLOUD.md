# Deploy to Streamlit Cloud (Easiest - Recommended)

Streamlit Cloud is the easiest way to deploy your chatbot for free!

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at https://share.streamlit.io)

## Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Insurance Policy Chatbot"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Create Streamlit Cloud App

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app/ui/streamlit_app.py`
6. Set branch: `main`

### 3. Configure Environment Variables

In Streamlit Cloud settings, add these secrets:

```
API_BASE_URL = http://localhost:8000
```

**Note:** For Streamlit Cloud, you have two options:

#### Option A: Deploy API Separately (Recommended)
- Deploy API to Railway/Render (see below)
- Set `API_BASE_URL` to your API URL

#### Option B: Run Everything in Streamlit (Simpler but slower)
- We'll modify the app to run the API internally
- No separate API server needed

### 4. Deploy!

Click "Deploy" and wait for it to build. Your app will be live at:
`https://YOUR_APP_NAME.streamlit.app`

## Option B: All-in-One Streamlit Deployment

If you want everything in one Streamlit app (no separate API), create this file:

`streamlit_app_simple.py`:
```python
"""Simplified Streamlit app that runs everything internally."""
import streamlit as st
from app.services.policy_service import PolicyService

# Initialize service
@st.cache_resource
def get_policy_service():
    return PolicyService()

policy_service = get_policy_service()

# Your existing Streamlit UI code, but call policy_service.query() directly
# instead of making HTTP requests
```

This runs everything in one process (simpler but slower for multiple users).
