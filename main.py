"""Main entry point for FastAPI application."""
import uvicorn
from app.api import create_app
from app.core.config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
