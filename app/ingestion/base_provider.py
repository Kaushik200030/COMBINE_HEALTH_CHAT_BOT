"""Base provider loader interface for extensibility."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseProviderLoader(ABC):
    """Abstract base class for insurance provider loaders."""
    
    def __init__(self, provider_name: str, base_url: str):
        self.provider_name = provider_name
        self.base_url = base_url
    
    @abstractmethod
    def fetch_index(self) -> List[Dict]:
        """Fetch the policy index page and extract policy listings."""
        pass
    
    @abstractmethod
    def fetch_document(self, url: str) -> bytes:
        """Download a policy document from URL."""
        pass
    
    @abstractmethod
    def parse_document(self, content: bytes, url: str, metadata: Dict) -> Dict:
        """Parse a document and extract structured content."""
        pass
    
    @abstractmethod
    def extract_metadata(self, policy_element: Dict) -> Dict:
        """Extract metadata from a policy listing element."""
        pass
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return self.provider_name
