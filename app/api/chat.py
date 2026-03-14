"""Chat API endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from app.services.policy_service import PolicyService
from app.core.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])

policy_service = PolicyService()


class ChatRequest(BaseModel):
    question: str
    filters: Optional[Dict] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict]
    confidence: str
    disclaimer: str


@router.post("/query", response_model=ChatResponse)
async def query_policy(request: ChatRequest):
    """Query the policy database."""
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        response = policy_service.query(request.question, filters=request.filters)
        
        return ChatResponse(**response)
        
    except Exception as e:
        logger.error(f"Error in chat query endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chat"}
