import numpy as np

class FaceMatcher:
    """Matches face embeddings using cosine similarity."""

    def __init__(self, threshold: float = 0.5):
        # A threshold of 0.5 is a highly reliable baseline for the buffalo_l model
        self.threshold = threshold

    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Computes the cosine similarity between two normalized embeddings.
        Returns a float between -1.0 and 1.0.
        """
        if emb1.shape != emb2.shape:
            raise ValueError(f"Embedding shape mismatch: {emb1.shape} vs {emb2.shape}")
            
        # Since our detector normalizes the vectors, dot product equals cosine similarity
        similarity = np.dot(emb1, emb2)
        return float(similarity)

    def is_match(self, emb1: np.ndarray, emb2: np.ndarray) -> bool:
        """Determines if two embeddings are from the same person based on the threshold."""
        return self.compute_similarity(emb1, emb2) >= self.threshold

if __name__ == "__main__":
    # Quick self-test to prove the math works
    print("Testing FaceMatcher...")
    matcher = FaceMatcher(threshold=0.5)
    
    # 1. Create two identical normalized vectors
    vec1 = np.ones(512)
    vec1 = vec1 / np.linalg.norm(vec1)
    
    vec2 = np.copy(vec1)
    
    # 2. Create a mathematically orthogonal vector (similarity should be exactly 0)
    vec3 = np.ones(512)
    vec3[:256] = -1.0 # Half positive, half negative cancels out the dot product
    vec3 = vec3 / np.linalg.norm(vec3)
    
    sim_identical = matcher.compute_similarity(vec1, vec2)
    sim_different = matcher.compute_similarity(vec1, vec3)
    
    print(f"Identical vectors similarity : {sim_identical:.4f} (Match: {matcher.is_match(vec1, vec2)})")
    print(f"Orthogonal vectors similarity: {sim_different:.4f} (Match: {matcher.is_match(vec1, vec3)})")