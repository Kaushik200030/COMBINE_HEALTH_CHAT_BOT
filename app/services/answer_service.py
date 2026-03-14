"""Service for generating answers from retrieved chunks."""
from typing import List, Dict, Optional
from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT, build_user_prompt, NO_RESULTS_PROMPT, AMBIGUOUS_QUERY_PROMPT
from app.core.logger import setup_logger
from app.services.llm_service import LLMService

logger = setup_logger(__name__)


class AnswerService:
    """Generate answers using free LLM with retrieved context."""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def generate_answer(self, query: str, context_chunks: List[Dict]) -> Dict:
        """Generate answer from query and context chunks."""
        try:
            # Handle no results
            if not context_chunks:
                return {
                    'answer': NO_RESULTS_PROMPT,
                    'sources': [],
                    'confidence': 'low',
                    'disclaimer': self._get_disclaimer()
                }
            
            # Check for ambiguous queries (multiple different policies)
            unique_policies = set(chunk.get('policy_title', '') for chunk in context_chunks)
            if len(unique_policies) > 3:
                policy_list = "\n".join([f"- {p}" for p in list(unique_policies)[:5]])
                return {
                    'answer': AMBIGUOUS_QUERY_PROMPT.format(policy_list=policy_list),
                    'sources': self._extract_sources(context_chunks),
                    'confidence': 'medium',
                    'disclaimer': self._get_disclaimer()
                }
            
            # Build prompt
            user_prompt = build_user_prompt(query, context_chunks)
            
            # Call LLM (free - Ollama or Hugging Face)
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
            
            answer = self.llm_service.generate(messages, temperature=0.1, max_tokens=1000)
            
            # Extract sources
            sources = self._extract_sources(context_chunks)
            
            # Determine confidence based on similarity scores
            avg_similarity = sum(chunk.get('similarity', 0) for chunk in context_chunks) / len(context_chunks)
            confidence = 'high' if avg_similarity > 0.85 else 'medium' if avg_similarity > 0.75 else 'low'
            
            return {
                'answer': answer,
                'sources': sources,
                'confidence': confidence,
                'disclaimer': self._get_disclaimer()
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                'answer': "I encountered an error while generating an answer. Please try again or rephrase your question.",
                'sources': [],
                'confidence': 'low',
                'disclaimer': self._get_disclaimer()
            }
    
    def _extract_sources(self, chunks: List[Dict]) -> List[Dict]:
        """Extract unique sources from chunks."""
        seen = set()
        sources = []
        
        for chunk in chunks:
            source_key = (
                chunk.get('policy_title', ''),
                chunk.get('source_url', '')
            )
            
            if source_key not in seen and source_key[0]:
                seen.add(source_key)
                sources.append({
                    'policy_title': chunk.get('policy_title', 'Unknown'),
                    'source_url': chunk.get('source_url', ''),
                    'effective_date': chunk.get('effective_date'),
                    'section_name': chunk.get('section_name', 'N/A'),
                    'procedure_codes': chunk.get('procedure_codes', [])
                })
        
        return sources
    
    def _get_disclaimer(self) -> str:
        """Get standard disclaimer text."""
        return """Note: This information is based on UnitedHealthcare commercial policy documents and is for informational purposes only. Coverage decisions depend on the member's specific benefit plan document, which may override policy guidance. Prior authorization requirements are maintained separately and should be verified. This does not constitute medical advice."""
