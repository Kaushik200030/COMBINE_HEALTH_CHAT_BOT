"""HTML document parser."""
from typing import Dict, List
from bs4 import BeautifulSoup
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class HTMLParser:
    """Parser for HTML policy documents."""
    
    def parse(self, content: bytes, url: str, metadata: Dict) -> Dict:
        """Parse HTML content and extract text with structure."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Extract main content
            main_content = soup.find(['main', 'article', 'div'], class_=lambda x: x and ('content' in x.lower() or 'main' in x.lower()))
            if not main_content:
                main_content = soup.find('body')
            
            if not main_content:
                main_content = soup
            
            # Extract sections
            sections = []
            current_section = None
            
            for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div']):
                tag_name = element.name
                text = element.get_text(strip=True)
                
                if not text:
                    continue
                
                # Headings indicate new sections
                if tag_name in ['h1', 'h2', 'h3', 'h4']:
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        'title': text,
                        'content': '',
                        'level': tag_name
                    }
                elif current_section:
                    current_section['content'] += text + "\n"
                else:
                    # Content before first heading
                    if not current_section:
                        current_section = {
                            'title': 'Introduction',
                            'content': '',
                            'level': 'p'
                        }
                    current_section['content'] += text + "\n"
            
            if current_section:
                sections.append(current_section)
            
            full_text = main_content.get_text(separator='\n', strip=True)
            
            return {
                'content': full_text,
                'metadata': metadata,
                'sections': sections
            }
            
        except Exception as e:
            logger.error(f"Error parsing HTML {url}: {e}")
            return {
                'content': '',
                'metadata': metadata,
                'sections': []
            }
