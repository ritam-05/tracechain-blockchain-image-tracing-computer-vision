import json
from typing import Dict, Any

class ContentCanonicalizer:
    """Serializes content metadata deterministically for hashing."""
    
    @staticmethod
    def canonicalize(metadata: Dict[str, str], image_hash: str = "") -> str:
        """
        Creates a deterministic JSON string from metadata and the image hash.
        Sorted keys ensure the output string is always identical for identical data.
        """
        # Combine metadata with the physical image fingerprint
        payload = {
            "title": metadata.get("title", ""),
            "url": metadata.get("url", ""),
            "platform": metadata.get("platform", ""),
            "image_hash": image_hash
        }
        
        # json.dumps with sort_keys=True ensures absolute determinism
        # separators=(',', ':') removes unnecessary whitespace padding
        return json.dumps(payload, sort_keys=True, separators=(',', ':'))

if __name__ == "__main__":
    # Quick self-test to prove determinism
    import sys
    import os
    # Ensure root directory is accessible for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from src.content.extractor import ContentExtractor
    
    print("Testing Content Extraction & Canonicalization...\n")
    
    mock_match = {
        "title": "   Hackathon Winner | Devpost   ", # Messy whitespace
        "source_url": "https://www.devpost.com/software/tracechain",
        "image_url": "https://example.com/image.jpg"
    }
    
    extractor = ContentExtractor()
    metadata = extractor.extract_metadata(mock_match)
    
    print("--- Extracted Metadata ---")
    print(json.dumps(metadata, indent=2))
    
    canonicalizer = ContentCanonicalizer()
    # We use a dummy hash for now. Step 10 will calculate the real image SHA-256.
    dummy_image_hash = "abc123def456..." 
    
    canonical_string = canonicalizer.canonicalize(metadata, dummy_image_hash)
    
    print("\n--- Canonical String (Ready for Blockchain Hashing) ---")
    print(canonical_string)