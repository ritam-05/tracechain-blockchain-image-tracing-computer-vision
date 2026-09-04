import os
import sys
from typing import List, Dict, Any, Optional
import numpy as np

# Ensure root directory is accessible for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.face.detector import FaceDetector

class FaceMatcher:
    """Matches face embeddings using cosine similarity and ranks candidate web matches."""

    def __init__(self, threshold: float = 0.5):
        # 0.5 is an optimal baseline threshold for InsightFace buffalo_l
        self.threshold = threshold

    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Computes the cosine similarity between two normalized embeddings.
        Returns a float between -1.0 and 1.0.
        """
        if emb1.shape != emb2.shape:
            raise ValueError(f"Embedding shape mismatch: {emb1.shape} vs {emb2.shape}")
            
        similarity = np.dot(emb1, emb2)
        return float(similarity)

    def is_match(self, emb1: np.ndarray, emb2: np.ndarray) -> bool:
        """Determines if two embeddings meet or exceed the similarity threshold."""
        return self.compute_similarity(emb1, emb2) >= self.threshold

    def match_candidates(
        self,
        query_embedding: np.ndarray,
        candidates: List[Dict[str, Any]],
        detector: FaceDetector
    ) -> List[Dict[str, Any]]:
        """
        Evaluates a list of downloaded candidates against the query embedding.
        Extracts faces from candidate images and computes similarity scores.
        """
        scored_candidates = []

        for cand in candidates:
            img_path = cand.get("local_path")
            if not img_path or not os.path.exists(img_path):
                continue

            try:
                # Detect face in candidate image
                result = detector.process_image(img_path)
                cand_embedding = result["embedding"]
                similarity = self.compute_similarity(query_embedding, cand_embedding)

                scored = cand.copy()
                scored["similarity"] = similarity
                scored["is_match"] = similarity >= self.threshold
                scored_candidates.append(scored)
                print(f"  Candidate [{cand['index']}] Similarity: {similarity:.4f} (Match: {scored['is_match']})")
            except ValueError:
                print(f"  Candidate [{cand['index']}] Skipped: No face detected in thumbnail.")
            except Exception as e:
                print(f"  Candidate [{cand['index']}] Skipped: Error processing image ({e}).")

        # Sort descending by similarity score
        scored_candidates.sort(key=lambda x: x["similarity"], reverse=True)
        return scored_candidates

    def select_best_match(self, scored_candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Selects the highest scoring candidate that meets the threshold."""
        if not scored_candidates:
            return None

        top_candidate = scored_candidates[0]
        if top_candidate["similarity"] >= self.threshold:
            return top_candidate
        return None


if __name__ == "__main__":
    print("Testing Candidate Face Matching Pipeline...")

    # 1. Locate query image
    query_path = os.path.join("data", "input", "test.jpg")
    if not os.path.exists(query_path):
        query_path = os.path.join("data", "input", "test.webp")

    detector = FaceDetector()
    matcher = FaceMatcher(threshold=0.5)

    print(f"\nProcessing query image: {query_path}")
    query_result = detector.process_image(query_path)
    query_embedding = query_result["embedding"]

    # 2. Gather candidates downloaded in Step 7
    candidates_dir = os.path.join("data", "candidates")
    mock_candidates = []
    if os.path.exists(candidates_dir):
        files = sorted(os.listdir(candidates_dir))
        for idx, filename in enumerate(files):
            if filename.endswith((".jpg", ".png", ".webp")):
                mock_candidates.append({
                    "index": idx + 1,
                    "title": f"Candidate Result {idx + 1}",
                    "source_url": "https://example.com",
                    "image_url": "https://example.com/image.jpg",
                    "local_path": os.path.join(candidates_dir, filename)
                })

    if not mock_candidates:
        print("✗ No candidate images found in 'data/candidates/'. Please run Step 7 first.")
        sys.exit(1)

    print(f"\nEvaluating {len(mock_candidates)} candidate thumbnails against query image...")
    scored = matcher.match_candidates(query_embedding, mock_candidates, detector)

    best_match = matcher.select_best_match(scored)
    if best_match:
        print(f"\n✓ BEST MATCH FOUND:")
        print(f"  Index     : Candidate [{best_match['index']}]")
        print(f"  Similarity: {best_match['similarity']:.4f}")
        print(f"  Path      : {best_match['local_path']}")
    else:
        print("\n✗ No candidate passed the verification threshold.")