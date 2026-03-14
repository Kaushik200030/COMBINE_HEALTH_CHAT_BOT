"""Embedding generation utilities using free sentence-transformers."""
from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class Embedder:
    """Generate embeddings using free sentence-transformers models."""
    
    def __init__(self):
        model_name = settings.embedding_model
        logger.info(f"Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            # Update config with actual dimension
            settings.embedding_dimension = self.dimension
            logger.info(f"Embedding model loaded. Dimension: {self.dimension}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            # Fallback to a smaller model
            logger.info("Falling back to default model: all-MiniLM-L6-v2")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.dimension = self.model.get_sentence_embedding_dimension()
            settings.embedding_dimension = self.dimension
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True, show_progress_bar=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches."""
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=True
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            # Fallback to individual embeddings
            embeddings = []
            for text in texts:
                try:
                    embeddings.append(self.embed_text(text))
                except:
                    # Return zero vector as fallback
                    embeddings.append([0.0] * self.dimension)
            return embeddings
