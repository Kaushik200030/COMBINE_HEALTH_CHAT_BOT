"""Health check endpoints."""
from fastapi import APIRouter
from app.retrieval.vectordb import VectorDB

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """General health check."""
    vector_db = VectorDB()
    if not vector_db.index:
        vector_db.load_index()  # Load index if not already loaded
    stats = vector_db.get_stats()
    
    return {
        "status": "healthy",
        "vector_db": {
            "loaded": stats['total_chunks'] > 0,
            "chunks": stats['total_chunks']
        }
    }
