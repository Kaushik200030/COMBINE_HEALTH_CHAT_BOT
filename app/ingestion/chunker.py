"""Text chunking utilities."""
from typing import List, Dict
import re
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class Chunker:
    """Chunk documents into smaller pieces for embedding."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        """Chunk a parsed document into smaller pieces."""
        content = document.get('content', '')
        metadata = document.get('metadata', {})
        sections = document.get('sections', [])
        
        chunks = []
        
        # If document has sections, chunk by section first
        if sections:
            for section in sections:
                section_chunks = self._chunk_text(
                    section.get('content', ''),
                    metadata={
                        **metadata,
                        'section_name': section.get('title', 'Unknown'),
                        'section_level': section.get('level', 'N/A'),
                        'page': section.get('page', None)
                    }
                )
                chunks.extend(section_chunks)
        else:
            # Chunk entire document
            chunks = self._chunk_text(content, metadata)
        
        return chunks
    
    def _chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Split text into chunks with overlap."""
        if not text:
            return []
        
        # Split by sentences first for better chunk boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed chunk size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'chunk_text': chunk_text,
                    **metadata,
                    'chunk_length': len(chunk_text)
                })
                
                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences + [sentence]
                current_length = sum(len(s) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'chunk_text': chunk_text,
                **metadata,
                'chunk_length': len(chunk_text)
            })
        
        return chunks
    
    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        """Get sentences for overlap based on chunk_overlap size."""
        if not sentences:
            return []
        
        overlap_text = ''
        overlap_sentences = []
        
        # Take sentences from the end until we reach overlap size
        for sentence in reversed(sentences):
            if len(overlap_text) + len(sentence) <= self.chunk_overlap:
                overlap_sentences.insert(0, sentence)
                overlap_text = sentence + ' ' + overlap_text
            else:
                break
        
        return overlap_sentences
