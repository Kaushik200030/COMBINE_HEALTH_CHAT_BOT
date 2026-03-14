"""API module."""
from fastapi import FastAPI
from app.api import chat, ingest, health
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Insurance Policy Chatbot API",
        description="RAG-based chatbot for UnitedHealthcare commercial policies",
        version="1.0.0"
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(ingest.router)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting Insurance Policy Chatbot API")
    
    return app
