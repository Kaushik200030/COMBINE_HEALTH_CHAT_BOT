"""Data ingestion API endpoints."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from app.ingestion.scraper import Scraper
from app.retrieval.vectordb import VectorDB
from app.core.logger import setup_logger
import json
from pathlib import Path
from app.core.config import settings

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


class IngestRequest(BaseModel):
    limit: Optional[int] = None
    provider: str = "UHC"


def ingest_policies(limit: int = None):
    """Background task for ingesting policies."""
    try:
        scraper = Scraper()
        chunks = scraper.scrape_all(limit=limit)
        
        # Add to vector database
        vector_db = VectorDB()
        if not vector_db.load_index():
            vector_db.create_index()
        
        vector_db.add_chunks(chunks)
        vector_db.save_index()
        
        logger.info(f"Ingestion complete: {len(chunks)} chunks added")
    except Exception as e:
        logger.error(f"Error in background ingestion: {e}")


@router.post("/start")
async def start_ingestion(request: IngestRequest, background_tasks: BackgroundTasks):
    """Start policy ingestion process."""
    try:
        background_tasks.add_task(ingest_policies, limit=request.limit)
        return {
            "status": "started",
            "message": "Ingestion process started in background"
        }
    except Exception as e:
        logger.error(f"Error starting ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_ingestion_status():
    """Get ingestion status."""
    try:
        vector_db = VectorDB()
        stats = vector_db.get_stats()
        
        processed_path = Path(settings.processed_data_path) / "chunks.json"
        has_processed_data = processed_path.exists()
        
        return {
            "vector_db_stats": stats,
            "has_processed_data": has_processed_data,
            "processed_data_path": str(processed_path) if has_processed_data else None
        }
    except Exception as e:
        logger.error(f"Error getting ingestion status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load-processed")
async def load_processed_data():
    """Load processed chunks into vector database."""
    try:
        processed_path = Path(settings.processed_data_path) / "chunks.json"
        
        if not processed_path.exists():
            raise HTTPException(status_code=404, detail="No processed data found")
        
        with open(processed_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        vector_db = VectorDB()
        if not vector_db.load_index():
            vector_db.create_index()
        
        vector_db.add_chunks(chunks)
        vector_db.save_index()
        
        return {
            "status": "success",
            "chunks_loaded": len(chunks)
        }
    except Exception as e:
        logger.error(f"Error loading processed data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
