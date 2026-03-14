#!/bin/bash

# Quick start script for Insurance Policy Chatbot

echo "🏥 Insurance Policy Chatbot - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        echo "⚠️  Warning: OPENAI_API_KEY not set in .env"
        echo "Please edit .env and add your OpenAI API key"
        echo ""
    fi
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/raw data/processed data/index

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Run: python scripts/ingest_data.py --limit 10"
echo "3. Start API: python main.py"
echo "4. Start UI: python run_streamlit.py"
echo ""
