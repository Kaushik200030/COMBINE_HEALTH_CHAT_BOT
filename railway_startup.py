"""Optional startup script for Railway to ensure data is loaded."""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.retrieval.vectordb import VectorDB
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def ensure_data_loaded():
    """Ensure vector database is loaded on Railway startup."""
    try:
        db = VectorDB()
        
        # Try to load existing index
        if db.load_index():
            logger.info(f"✅ Vector database loaded: {len(db.metadata)} chunks")
            return True
        
        # If no index, try to load from processed chunks
        processed_path = Path("data/processed/chunks.json")
        if processed_path.exists():
            logger.info("Loading chunks from processed data...")
            import json
            with open(processed_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            db.add_chunks(chunks)
            db.save_index()
            logger.info(f"✅ Loaded {len(chunks)} chunks into vector database")
            return True
        else:
            logger.warning("No vector database or processed chunks found")
            logger.info("You may need to ingest data first")
            return False
            
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return False


if __name__ == "__main__":
    ensure_data_loaded()
