"""PDF document parser."""
import re
from typing import Dict, List
import fitz  # PyMuPDF
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class PDFParser:
    """Parser for PDF policy documents."""
    
    def parse(self, content: bytes, url: str, metadata: Dict) -> Dict:
        """Parse PDF content and extract text with structure."""
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            
            full_text = []
            sections = []
            current_section = None
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                full_text.append(text)
                
                # Try to identify sections (headings are often larger or bold)
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if "lines" in block:
                        for line in block["lines"]:
                            line_text = "".join([span.get("text", "") for span in line.get("spans", [])])
                            line_text = line_text.strip()
                            
                            # Heuristic: lines in all caps or with specific patterns might be headings
                            if line_text and (
                                line_text.isupper() or
                                re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$', line_text) or
                                re.match(r'^\d+\.\s+[A-Z]', line_text)
                            ):
                                if current_section:
                                    sections.append(current_section)
                                current_section = {
                                    'title': line_text,
                                    'content': '',
                                    'page': page_num + 1
                                }
                            elif current_section:
                                current_section['content'] += line_text + "\n"
            
            if current_section:
                sections.append(current_section)
            
            return {
                'content': "\n\n".join(full_text),
                'metadata': metadata,
                'sections': sections,
                'page_count': len(doc)
            }
            
        except Exception as e:
            logger.error(f"Error parsing PDF {url}: {e}")
            return {
                'content': '',
                'metadata': metadata,
                'sections': [],
                'page_count': 0
            }
