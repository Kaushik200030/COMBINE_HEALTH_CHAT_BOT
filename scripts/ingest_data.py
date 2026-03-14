"""Script to ingest policy data."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingestion.scraper import Scraper
from app.retrieval.vectordb import VectorDB
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main ingestion script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest UHC policy data")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of policies to process")
    parser.add_argument("--load-existing", action="store_true", help="Load existing processed data")
    
    args = parser.parse_args()
    
    # Load existing processed data if requested
    if args.load_existing:
        logger.info("Loading existing processed data...")
        from pathlib import Path
        import json
        from app.core.config import settings
        
        processed_path = Path(settings.processed_data_path) / "chunks.json"
        if processed_path.exists():
            with open(processed_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            vector_db = VectorDB()
            if not vector_db.load_index():
                vector_db.create_index()
            
            vector_db.add_chunks(chunks)
            vector_db.save_index()
            logger.info(f"Loaded {len(chunks)} chunks into vector database")
        else:
            logger.error("No processed data found. Run without --load-existing first.")
        return
    
    # Scrape new data
    logger.info("Starting data ingestion...")
    scraper = Scraper()
    chunks = scraper.scrape_all(limit=args.limit)
    
    # Add to vector database
    logger.info("Adding chunks to vector database...")
    vector_db = VectorDB()
    if not vector_db.load_index():
        vector_db.create_index()
    
    vector_db.add_chunks(chunks)
    vector_db.save_index()
    
    logger.info(f"Ingestion complete: {len(chunks)} chunks added to vector database")


if __name__ == "__main__":
    main()
