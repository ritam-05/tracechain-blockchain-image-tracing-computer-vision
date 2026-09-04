import os
from typing import Dict, Any, List
import cv2
import numpy as np
from insightface.app import FaceAnalysis

class FaceDetector:
    """Handles face detection and feature extraction using InsightFace."""

    def __init__(self, model_name: str = "buffalo_l", det_size: tuple = (640, 640)):
        # CPUExecutionProvider ensures portability without requiring GPU configurations
        self.app = FaceAnalysis(name=model_name, providers=["CPUExecutionProvider"])
        self.app.prepare(ctx_id=0, det_size=det_size)

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Loads an image from path, detects faces, and extracts the primary face embedding.
        
        Returns:
            dict containing:
                - 'face_count': int
                - 'embedding': np.ndarray (512,)
                - 'bbox': List[int] [x1, y1, x2, y2]
                - 'score': float
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Failed to decode image from path: {image_path}")

        return self.extract_from_bgr(img)

    def extract_from_bgr(self, img: np.ndarray) -> Dict[str, Any]:
        """
        Detects faces in a raw OpenCV BGR image and extracts the primary embedding.
        """
        faces = self.app.get(img)

        if len(faces) == 0:
            raise ValueError("No face detected in the provided image.")

        # Sort by bounding box area (largest face is selected as the primary subject)
        faces_sorted = sorted(
            faces,
            key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
            reverse=True
        )
        primary_face = faces_sorted[0]

        # Normalize the embedding vector to unit length for cosine similarity
        embedding = primary_face.embedding
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return {
            "face_count": len(faces),
            "bbox": primary_face.bbox.astype(int).tolist(),
            "score": float(primary_face.det_score),
            "embedding": embedding
        }

if __name__ == "__main__":
    # Quick self-test
    sample_path = os.path.join("data", "input", "test.webp")
    if not os.path.exists(sample_path):
        sample_path = os.path.join("data", "input", "test.jpg")
        
    print(f"Testing FaceDetector with {sample_path}...")
    detector = FaceDetector()
    result = detector.process_image(sample_path)
    
    print("\n--- Detection Result ---")
    print(f"Face Count   : {result['face_count']}")
    print(f"Primary Box  : {result['bbox']}")
    print(f"Confidence   : {result['score']:.4f}")
    print(f"Embedding Dim: {result['embedding'].shape}")
    print("Vector Norm  : {:.4f} (expected: ~1.0)".format(np.linalg.norm(result["embedding"])))