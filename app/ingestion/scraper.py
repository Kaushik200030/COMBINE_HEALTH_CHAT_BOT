"""Main scraper orchestrator."""
import os
import json
from typing import List, Dict
from pathlib import Path
from app.ingestion.uhc_provider import UHCProviderLoader
from app.ingestion.chunker import Chunker
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class Scraper:
    """Main scraper for ingesting policy documents."""
    
    def __init__(self, provider_loader=None):
        self.provider_loader = provider_loader or UHCProviderLoader()
        self.chunker = Chunker()
        self.raw_data_path = Path(settings.raw_data_path)
        self.processed_data_path = Path(settings.processed_data_path)
        
        # Create directories
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.processed_data_path.mkdir(parents=True, exist_ok=True)
    
    def scrape_all(self, limit: int = None) -> List[Dict]:
        """Scrape all policies from the provider."""
        logger.info(f"Starting scrape for {self.provider_loader.get_provider_name()}")
        
        # Fetch policy index
        policies = self.provider_loader.fetch_index()
        
        if limit:
            policies = policies[:limit]
        
        logger.info(f"Found {len(policies)} policies to process")
        
        all_chunks = []
        
        for idx, policy_meta in enumerate(policies, 1):
            try:
                logger.info(f"Processing policy {idx}/{len(policies)}: {policy_meta.get('title', 'Unknown')}")
                
                # Download document
                url = policy_meta['url']
                content = self.provider_loader.fetch_document(url)
                
                # Save raw document
                doc_filename = f"policy_{idx}_{policy_meta.get('title', 'unknown')[:50]}.pdf"
                doc_path = self.raw_data_path / doc_filename
                doc_path.write_bytes(content)
                
                # Parse document
                parsed_doc = self.provider_loader.parse_document(content, url, policy_meta)
                
                # Chunk document
                chunks = self.chunker.chunk_document(parsed_doc)
                
                # Add source URL to each chunk
                for chunk in chunks:
                    chunk['source_url'] = url
                    chunk['policy_title'] = policy_meta.get('title', 'Unknown')
                
                all_chunks.extend(chunks)
                
                logger.info(f"Created {len(chunks)} chunks from policy {idx}")
                
            except Exception as e:
                logger.error(f"Error processing policy {idx}: {e}")
                continue
        
        # Save processed chunks
        output_file = self.processed_data_path / "chunks.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Scraping complete. Created {len(all_chunks)} total chunks")
        return all_chunks
