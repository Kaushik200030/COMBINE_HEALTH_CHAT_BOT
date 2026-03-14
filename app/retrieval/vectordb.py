"""Vector database management."""
import os
import json
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path
from app.core.config import settings
from app.core.logger import setup_logger
from app.retrieval.embedder import Embedder

logger = setup_logger(__name__)

# Try to import FAISS, with fallback
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not available. Using fallback vector store.")


class VectorDB:
    """FAISS-based vector database for storing and retrieving document chunks."""
    
    def __init__(self):
        self.db_path = Path(settings.vector_db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.db_path / "faiss.index"
        self.metadata_path = self.db_path / "metadata.json"
        self.embedder = Embedder()
        self.index = None
        self.metadata = []
        self.dimension = settings.embedding_dimension  # From embedding model
    
    def create_index(self):
        """Create a new FAISS index or fallback."""
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatL2(self.dimension)
            logger.info("Created new FAISS index")
        else:
            # Fallback: use numpy array for vectors
            self.index = None
            self.vectors = []
            logger.info("Using numpy-based fallback vector store")
        self.metadata = []
    
    def load_index(self) -> bool:
        """Load existing index from disk."""
        try:
            if self.index_path.exists() and self.metadata_path.exists():
                if FAISS_AVAILABLE:
                    self.index = faiss.read_index(str(self.index_path))
                else:
                    # Fallback: load vectors from metadata
                    self.index = None
                    self.vectors = []
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded index with {len(self.metadata)} vectors")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False
    
    def save_index(self):
        """Save index and metadata to disk."""
        try:
            if FAISS_AVAILABLE and self.index:
                faiss.write_index(self.index, str(self.index_path))
            # Always save metadata
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved index with {len(self.metadata)} vectors")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def add_chunks(self, chunks: List[Dict]):
        """Add document chunks to the vector database."""
        if not self.index and not hasattr(self, 'vectors'):
            self.create_index()
        
        texts = [chunk['chunk_text'] for chunk in chunks]
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        
        embeddings = self.embedder.embed_batch(texts)
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to index
        if FAISS_AVAILABLE and self.index:
            self.index.add(embeddings_array)
        else:
            # Fallback: store in list
            if not hasattr(self, 'vectors'):
                self.vectors = []
            self.vectors.extend(embeddings_array.tolist())
        
        # Store metadata
        for i, chunk in enumerate(chunks):
            self.metadata.append({
                'chunk_id': len(self.metadata),
                'chunk_text': chunk['chunk_text'],
                'policy_title': chunk.get('policy_title', 'Unknown'),
                'section_name': chunk.get('section_name', 'N/A'),
                'source_url': chunk.get('source_url', ''),
                'effective_date': chunk.get('effective_date'),
                'published_date': chunk.get('published_date'),
                'procedure_codes': chunk.get('procedure_codes', []),
                'provider_name': chunk.get('provider_name', 'Unknown')
            })
        
        # Re-index keyword search if it exists
        # This will be done by the retriever when it initializes
        
        logger.info(f"Added {len(chunks)} chunks to vector database")
    
    def search(self, query: str, top_k: int = None, threshold: float = None) -> List[Dict]:
        """Search for similar chunks."""
        if len(self.metadata) == 0:
            return []
        
        top_k = top_k or settings.top_k_chunks
        threshold = threshold or settings.similarity_threshold
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        query_vector = np.array(query_embedding).astype('float32')
        
        if FAISS_AVAILABLE and self.index:
            # Use FAISS search
            k = min(top_k, len(self.metadata))
            distances, indices = self.index.search(np.array([query_vector]), k)
            
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.metadata):
                    similarity = 1 / (1 + distance)
                    if similarity >= threshold:
                        result = self.metadata[idx].copy()
                        result['similarity'] = float(similarity)
                        result['distance'] = float(distance)
                        results.append(result)
        else:
            # Fallback: numpy-based search
            if not hasattr(self, 'vectors') or len(self.vectors) == 0:
                return []
            
            vectors_array = np.array(self.vectors).astype('float32')
            # Compute L2 distances
            distances = np.linalg.norm(vectors_array - query_vector, axis=1)
            # Get top_k indices
            k = min(top_k, len(distances))
            indices = np.argsort(distances)[:k]
            
            results = []
            for idx in indices:
                distance = float(distances[idx])
                similarity = 1 / (1 + distance)
                if similarity >= threshold and idx < len(self.metadata):
                    result = self.metadata[idx].copy()
                    result['similarity'] = float(similarity)
                    result['distance'] = distance
                    results.append(result)
        
        return results
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        return {
            'total_chunks': len(self.metadata) if self.metadata else 0,
            'index_type': type(self.index).__name__ if self.index else None,
            'dimension': self.dimension
        }
