import cv2
import os
from insightface.app import FaceAnalysis

def main():
    # 1. Setup directories and input image
    os.makedirs('data/input', exist_ok=True)
    img_path = 'data/input/test.webp'
    
    if not os.path.exists(img_path):
        print(f"✗ ERROR: Image not found at {img_path}")
        print("Please manually place a photo of a person in the data/input/ folder and name it 'test.jpg'.")
        return

    # 2. Initialize InsightFace
    print("\nInitializing InsightFace...")
    print("(Note: On the first run, this will download the ~330MB 'buffalo_l' model to your home directory.)")
    
    # We explicitly use CPUExecutionProvider to ensure it runs universally without needing CUDA drivers right now
    app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    # 3. Load and process image
    print(f"\nLoading image from {img_path}...")
    img = cv2.imread(img_path)
    
    if img is None:
        print("✗ ERROR: Could not read image. Ensure it is a valid JPG/PNG file.")
        return

    print("Detecting faces...")
    faces = app.get(img)

    # 4. Output results
    if len(faces) == 0:
        print("✗ ERROR: No faces detected in the image!")
    else:
        print(f"\n✓ SUCCESS: {len(faces)} face(s) detected.")
        
        # Display details of the first detected face
        box = faces[0].bbox.astype(int)
        score = faces[0].det_score
        print(f"  Face 1 -> Bounding Box: {box}, Confidence Score: {score:.4f}")
        print(f"  Embedding Shape: {faces[0].embedding.shape} (This is the mathematical fingerprint!)")

if __name__ == "__main__":
    main()