import urllib.parse
from typing import Dict, Any

class ContentExtractor:
    """Extracts and normalizes metadata from a matched search result."""
    
    @staticmethod
    def extract_metadata(match_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Parses the raw match dictionary (from SerpApi/Matcher) 
        and extracts clean, standard metadata.
        """
        url = match_data.get("source_url", "")
        
        # Extract domain as platform (e.g., 'www.linkedin.com' -> 'linkedin')
        platform = "unknown"
        if url:
            parsed_uri = urllib.parse.urlparse(url)
            domain = parsed_uri.netloc.replace("www.", "")
            platform = domain.split('.')[0] if domain else "unknown"

        return {
            "title": match_data.get("title", "Untitled").strip(),
            "url": url.strip(),
            "platform": platform,
            "image_url": match_data.get("image_url", "").strip()
        }