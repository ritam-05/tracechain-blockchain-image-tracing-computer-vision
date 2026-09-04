import hashlib
import os

class Hasher:
    """Generates SHA-256 cryptographic hashes for files and strings."""

    @staticmethod
    def hash_file(filepath: str) -> str:
        """
        Calculates the SHA-256 hash of a file.
        Reads in chunks to handle potentially large files efficiently.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Cannot hash missing file: {filepath}")

        sha256_hash = hashlib.sha256()
        
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
                
        return sha256_hash.hexdigest()

    @staticmethod
    def hash_string(data: str) -> str:
        """Calculates the SHA-256 hash of a string (like our canonical JSON)."""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        return sha256_hash.hexdigest()

if __name__ == "__main__":
    import sys
    # Ensure root directory is accessible for imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from src.content.canonicalizer import ContentCanonicalizer
    
    print("Testing Cryptographic Hashing...\n")
    
    # 1. Test File Hashing (using our test input image)
    sample_path = os.path.join("data", "input", "test.jpg")
    if not os.path.exists(sample_path):
        sample_path = os.path.join("data", "input", "test.webp")
        
    try:
        image_hash = Hasher.hash_file(sample_path)
        print(f"✓ Image Hash ({os.path.basename(sample_path)}):")
        print(f"  {image_hash}")
        
        # 2. Test Content Fingerprinting
        mock_metadata = {
            "title": "Hackathon Winner | Devpost",
            "url": "https://www.devpost.com/software/tracechain",
            "platform": "devpost"
        }
        
        canonical_string = ContentCanonicalizer.canonicalize(mock_metadata, image_hash)
        final_fingerprint = Hasher.hash_string(canonical_string)
        
        print("\n✓ Final Content Fingerprint (To be stored on-chain):")
        print(f"  0x{final_fingerprint}")
        
    except Exception as e:
        print(f"✗ ERROR: {e}")