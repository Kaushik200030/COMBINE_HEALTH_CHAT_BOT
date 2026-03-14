"""Keyword-based search using BM25/TF-IDF."""
from typing import List, Dict
import re
from collections import Counter
import math
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class BM25Search:
    """BM25 keyword search implementation."""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        Initialize BM25 search.
        
        Args:
            k1: Term frequency saturation parameter
            b: Length normalization parameter
        """
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_freqs = []
        self.idf = {}
        self.avg_doc_len = 0
    
    def index_documents(self, documents: List[Dict]):
        """Index documents for BM25 search."""
        self.documents = documents
        
        # Tokenize and compute document frequencies
        doc_tokens = []
        doc_lengths = []
        
        for doc in documents:
            tokens = self._tokenize(doc.get('chunk_text', ''))
            doc_tokens.append(tokens)
            doc_lengths.append(len(tokens))
        
        # Compute average document length
        self.avg_doc_len = sum(doc_lengths) / len(doc_lengths) if doc_lengths else 0
        
        # Compute document frequencies
        df = Counter()
        for tokens in doc_tokens:
            df.update(set(tokens))
        
        # Compute IDF
        N = len(documents)
        for term, freq in df.items():
            self.idf[term] = math.log((N - freq + 0.5) / (freq + 0.5) + 1.0)
        
        self.doc_freqs = doc_tokens
        logger.info(f"Indexed {len(documents)} documents for BM25 search")
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Convert to lowercase and split on non-word characters
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search documents using BM25."""
        if not self.documents:
            return []
        
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        
        scores = []
        
        for i, doc in enumerate(self.documents):
            score = self._bm25_score(query_tokens, i)
            if score > 0:
                scores.append((score, i, doc))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Return top_k results
        results = []
        for score, idx, doc in scores[:top_k]:
            result = doc.copy()
            result['bm25_score'] = float(score)
            results.append(result)
        
        return results
    
    def _bm25_score(self, query_tokens: List[str], doc_idx: int) -> float:
        """Calculate BM25 score for a document."""
        score = 0.0
        doc_tokens = self.doc_freqs[doc_idx]
        doc_len = len(doc_tokens)
        
        for term in query_tokens:
            if term not in self.idf:
                continue
            
            # Term frequency in document
            tf = doc_tokens.count(term)
            
            if tf == 0:
                continue
            
            # BM25 formula
            idf = self.idf[term]
            numerator = idf * tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len))
            score += numerator / denominator
        
        return score


class KeywordSearch:
    """Simple keyword search wrapper."""
    
    def __init__(self):
        self.bm25 = BM25Search()
        self.indexed = False
    
    def index(self, documents: List[Dict]):
        """Index documents for keyword search."""
        self.bm25.index_documents(documents)
        self.indexed = True
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search using keyword matching."""
        if not self.indexed:
            logger.warning("Keyword search not indexed. Returning empty results.")
            return []
        
        return self.bm25.search(query, top_k=top_k)
