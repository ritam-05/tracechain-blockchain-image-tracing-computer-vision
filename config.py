import os
from dotenv import load_dotenv

# Load variables from .env into the system environment
load_dotenv()

class Config:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")

    @classmethod
    def validate_serpapi(cls):
        """Ensures the SerpApi key is present and not the default placeholder."""
        if not cls.SERPAPI_KEY or "paste_your" in cls.SERPAPI_KEY:
            raise ValueError("✗ SERPAPI_KEY is missing or invalid in the .env file. Please add your actual key.")
        return True

if __name__ == "__main__":
    # Quick self-test to verify the key works with SerpApi
    from serpapi import GoogleSearch
    print("Loading configuration...")
    
    try:
        Config.validate_serpapi()
        print("✓ API key found in .env")
        
        print("Testing SerpApi authentication...")
        # A lightweight text search just to test the credentials
        params = {
            "q": "Hackathon",
            "api_key": Config.SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            print(f"✗ SerpApi Error: {results['error']}")
        else:
            print("✓ SUCCESS: SerpApi key is valid and authenticated!")
            
    except Exception as e:
        print(e)