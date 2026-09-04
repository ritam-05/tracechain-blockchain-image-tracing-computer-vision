import os
import sys
import json
import urllib.request
from typing import Dict, Any, List
from serpapi import GoogleSearch

# Ensure the root directory is in the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import Config

class LensSearch:
    """Handles reverse image searching via SerpApi Google Lens and candidate downloads."""

    def __init__(self, candidates_dir: str = os.path.join("data", "candidates")):
        self.api_key = Config.SERPAPI_KEY
        self.candidates_dir = candidates_dir
        os.makedirs(self.candidates_dir, exist_ok=True)

    def upload_image(self, image_path: str) -> str:
        """Uploads a local image to SerpApi to obtain a temporary image_id for searching."""
        url = "https://serpapi.com/image"
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="api_key"\r\n\r\n'
            f"{self.api_key}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="image"; filename="image.jpg"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode('utf-8') + image_data + f"\r\n--{boundary}--\r\n".encode('utf-8')

        req = urllib.request.Request(url, data=body)
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.loads(response.read().decode('utf-8'))
            if "image_id" not in res:
                raise ValueError(f"Failed to upload image to SerpApi: {res}")
            return res["image_id"]

    def search(self, image_path: str) -> Dict[str, Any]:
        """Executes a full Google Lens search on the provided image."""
        print(f"  -> Uploading {image_path} to SerpApi...")
        image_id = self.upload_image(image_path)
        
        print(f"  -> Upload successful (ID: {image_id}). Querying Google Lens...")
        params = {
            "engine": "google_lens",
            "image_id": image_id,
            "api_key": self.api_key,
            "hl": "en"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            raise RuntimeError(f"SerpApi Error: {results['error']}")
            
        return results

    def extract_candidates(self, results: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Parses visual matches from SerpApi results up to the specified limit."""
        matches = results.get("visual_matches", [])
        candidates = []
        
        for idx, match in enumerate(matches[:limit]):
            # Use thumbnail or high-res image URL if available
            image_url = match.get("thumbnail") or match.get("original")
            if not image_url:
                continue

            candidates.append({
                "index": idx + 1,
                "title": match.get("title", "Untitled Match"),
                "source_url": match.get("link", ""),
                "image_url": image_url,
                "local_path": None
            })
            
        return candidates

    def download_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Downloads candidate images locally so InsightFace can inspect them.
        Skips invalid URLs or failed downloads without terminating the program.
        """
        downloaded = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TraceChain/1.0"}

        for candidate in candidates:
            idx = candidate["index"]
            url = candidate["image_url"]
            filename = f"candidate_{idx}.jpg"
            target_path = os.path.join(self.candidates_dir, filename)

            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp, open(target_path, "wb") as out:
                    out.write(resp.read())
                    
                candidate["local_path"] = target_path
                downloaded.append(candidate)
                print(f"  ✓ Downloaded candidate [{idx}]: {filename}")
            except Exception as e:
                print(f"  ✗ Failed to download candidate [{idx}] from {url}: {e}")

        return downloaded


if __name__ == "__main__":
    print("Testing Candidate Retrieval & Image Download...")

    sample_path = os.path.join("data", "input", "test.jpg")
    if not os.path.exists(sample_path):
        sample_path = os.path.join("data", "input", "test.webp")

    lens = LensSearch()
    results = lens.search(sample_path)
    candidates = lens.extract_candidates(results, limit=5)
    
    print(f"\nExtracted {len(candidates)} candidate match records.")
    print("Downloading candidate images...")
    successful_downloads = lens.download_candidates(candidates)
    
    print(f"\n✓ Successfully downloaded {len(successful_downloads)} candidate images into 'data/candidates/'.")