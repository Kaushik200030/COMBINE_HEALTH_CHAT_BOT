"""UnitedHealthcare provider loader implementation."""
import re
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from app.ingestion.base_provider import BaseProviderLoader
from app.core.logger import setup_logger
from app.ingestion.pdf_parser import PDFParser
from app.ingestion.html_parser import HTMLParser

logger = setup_logger(__name__)


class UHCProviderLoader(BaseProviderLoader):
    """Loader for UnitedHealthcare commercial policies."""
    
    def __init__(self):
        super().__init__(
            provider_name="UnitedHealthcare",
            base_url="https://www.uhcprovider.com"
        )
        self.pdf_parser = PDFParser()
        self.html_parser = HTMLParser()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_index(self) -> List[Dict]:
        """Fetch UHC commercial policies index page."""
        try:
            url = f"{self.base_url}/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            policies = []
            
            # Find policy cards/listings - adjust selectors based on actual page structure
            policy_cards = soup.find_all(['div', 'article'], class_=re.compile(r'policy|card|listing', re.I))
            
            for card in policy_cards:
                try:
                    # Extract policy title
                    title_elem = card.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|heading', re.I))
                    if not title_elem:
                        title_elem = card.find(['h2', 'h3', 'h4', 'a'])
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Extract link
                    link_elem = card.find('a', href=True)
                    if not link_elem:
                        continue
                    
                    href = link_elem['href']
                    if not href.startswith('http'):
                        href = f"{self.base_url}{href}" if href.startswith('/') else f"{self.base_url}/{href}"
                    
                    # Extract metadata
                    metadata = self.extract_metadata(card)
                    metadata['title'] = title
                    metadata['url'] = href
                    
                    policies.append(metadata)
                    
                except Exception as e:
                    logger.warning(f"Error parsing policy card: {e}")
                    continue
            
            logger.info(f"Found {len(policies)} policies from index page")
            return policies
            
        except Exception as e:
            logger.error(f"Error fetching index: {e}")
            return []
    
    def fetch_document(self, url: str) -> bytes:
        """Download a policy document."""
        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error fetching document {url}: {e}")
            raise
    
    def parse_document(self, content: bytes, url: str, metadata: Dict) -> Dict:
        """Parse a document (PDF or HTML)."""
        try:
            if url.endswith('.pdf') or 'pdf' in url.lower():
                return self.pdf_parser.parse(content, url, metadata)
            else:
                return self.html_parser.parse(content, url, metadata)
        except Exception as e:
            logger.error(f"Error parsing document {url}: {e}")
            return {
                'content': '',
                'metadata': metadata,
                'sections': []
            }
    
    def extract_metadata(self, policy_element) -> Dict:
        """Extract metadata from a policy listing element."""
        metadata = {
            'provider_name': self.provider_name,
            'policy_type': 'commercial',
            'effective_date': None,
            'published_date': None,
            'procedure_codes': [],
            'drug_codes': [],
            'category': None
        }
        
        text = policy_element.get_text()
        
        # Extract dates (common patterns)
        date_patterns = [
            r'effective[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'published[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                if 'effective' in pattern.lower():
                    metadata['effective_date'] = match.group(1)
                elif 'published' in pattern.lower():
                    metadata['published_date'] = match.group(1)
                elif not metadata['effective_date']:
                    metadata['effective_date'] = match.group(1)
        
        # Extract procedure codes (CPT/HCPCS)
        code_patterns = [
            r'\b(\d{5})\b',  # 5-digit codes
            r'CPT[:\s]+(\d{5})',
            r'HCPCS[:\s]+([A-Z]\d{4})',
        ]
        
        codes = []
        for pattern in code_patterns:
            matches = re.findall(pattern, text, re.I)
            codes.extend(matches)
        
        metadata['procedure_codes'] = list(set(codes[:10]))  # Limit to 10 codes
        
        return metadata
