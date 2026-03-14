"""Service for policy-related operations."""
from typing import List, Dict
from app.retrieval.retriever import Retriever
from app.services.answer_service import AnswerService
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class PolicyService:
    """Main service for policy queries."""
    
    def __init__(self):
        self.retriever = Retriever()
        self.answer_service = AnswerService()
    
    def query(self, question: str, filters: Dict = None) -> Dict:
        """Query the policy database and generate an answer."""
        try:
            # Retrieve relevant chunks
            chunks = self.retriever.retrieve(question, filters=filters)
            
            # Format for prompt
            formatted_chunks = self.retriever.format_results_for_prompt(chunks)
            
            # Generate answer
            response = self.answer_service.generate_answer(question, formatted_chunks)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in policy query: {e}")
            return {
                'answer': "I encountered an error processing your question. Please try again.",
                'sources': [],
                'confidence': 'low',
                'disclaimer': self.answer_service._get_disclaimer()
            }
