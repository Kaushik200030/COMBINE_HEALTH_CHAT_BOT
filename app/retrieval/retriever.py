"""Retrieval logic for finding relevant policy chunks."""
from typing import List, Dict
from app.retrieval.vectordb import VectorDB
from app.retrieval.keyword_search import KeywordSearch
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class Retriever:
    """Retrieve relevant policy chunks for queries using hybrid search."""
    
    def __init__(self, vector_db: VectorDB = None):
        self.vector_db = vector_db or VectorDB()
        if not self.vector_db.index:
            self.vector_db.load_index()
        
        # Initialize keyword search
        self.keyword_search = KeywordSearch()
        self._index_keyword_search()
    
    def _index_keyword_search(self):
        """Index documents for keyword search."""
        try:
            if self.vector_db.metadata:
                self.keyword_search.index(self.vector_db.metadata)
                logger.info("Keyword search indexed successfully")
        except Exception as e:
            logger.warning(f"Could not index keyword search: {e}")
    
    def retrieve(self, query: str, top_k: int = None, filters: Dict = None) -> List[Dict]:
        """Retrieve relevant chunks using hybrid search (semantic + keyword)."""
        try:
            top_k = top_k or settings.top_k_chunks
            
            if settings.hybrid_search_enabled:
                # Hybrid search: combine semantic and keyword results
                results = self._hybrid_search(query, top_k)
            else:
                # Semantic search only
                results = self.vector_db.search(query, top_k=top_k)
            
            # Apply filters if provided
            if filters:
                results = self._apply_filters(results, filters)
            
            # Sort by combined score
            results.sort(key=lambda x: x.get('combined_score', x.get('similarity', 0)), reverse=True)
            
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            return []
    
    def _hybrid_search(self, query: str, top_k: int) -> List[Dict]:
        """Perform hybrid search combining semantic and keyword results."""
        # Get semantic search results
        semantic_results = self.vector_db.search(query, top_k=top_k * 2)
        
        # Get keyword search results
        keyword_results = self.keyword_search.search(query, top_k=top_k * 2)
        
        # Create a map of chunk_id to results for merging
        combined = {}
        
        # Process semantic results
        for result in semantic_results:
            chunk_id = result.get('chunk_id')
            if chunk_id is not None:
                combined[chunk_id] = result.copy()
                combined[chunk_id]['semantic_score'] = result.get('similarity', 0)
                combined[chunk_id]['keyword_score'] = 0.0
        
        # Process keyword results and merge
        max_bm25 = max([r.get('bm25_score', 0) for r in keyword_results], default=1.0) if keyword_results else 1.0
        
        for result in keyword_results:
            chunk_id = result.get('chunk_id')
            if chunk_id is not None:
                # Normalize BM25 score to 0-1 range
                normalized_bm25 = result.get('bm25_score', 0) / max_bm25 if max_bm25 > 0 else 0
                
                if chunk_id in combined:
                    # Merge with existing semantic result
                    combined[chunk_id]['keyword_score'] = normalized_bm25
                else:
                    # New result from keyword search
                    combined[chunk_id] = result.copy()
                    combined[chunk_id]['semantic_score'] = 0.0
                    combined[chunk_id]['keyword_score'] = normalized_bm25
                    combined[chunk_id]['similarity'] = 0.0
        
        # Calculate combined scores
        alpha = settings.hybrid_search_alpha  # Weight for semantic search
        beta = 1.0 - alpha  # Weight for keyword search
        
        results = []
        for chunk_id, result in combined.items():
            semantic_score = result.get('semantic_score', 0)
            keyword_score = result.get('keyword_score', 0)
            
            # Combined score: weighted average
            combined_score = (alpha * semantic_score) + (beta * keyword_score)
            result['combined_score'] = combined_score
            result['similarity'] = combined_score  # For backward compatibility
            
            results.append(result)
        
        return results
    
    def _apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Apply metadata filters to results."""
        filtered = []
        
        for result in results:
            match = True
            
            if 'provider_name' in filters:
                if result.get('provider_name') != filters['provider_name']:
                    match = False
            
            if 'policy_title' in filters:
                if filters['policy_title'].lower() not in result.get('policy_title', '').lower():
                    match = False
            
            if 'procedure_code' in filters:
                codes = result.get('procedure_codes', [])
                if filters['procedure_code'] not in codes:
                    match = False
            
            if match:
                filtered.append(result)
        
        return filtered
    
    def format_results_for_prompt(self, results: List[Dict]) -> List[Dict]:
        """Format retrieval results for LLM prompt."""
        formatted = []
        
        for result in results:
            formatted.append({
                'policy_title': result.get('policy_title', 'Unknown'),
                'section_name': result.get('section_name', 'N/A'),
                'source_url': result.get('source_url', ''),
                'effective_date': result.get('effective_date'),
                'chunk_text': result.get('chunk_text', ''),
                'procedure_codes': result.get('procedure_codes', []),
                'similarity': result.get('similarity', 0)
            })
        
        return formatted
