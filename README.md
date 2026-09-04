# TraceChain Face Matching Core

This repository provides the face-processing core for TraceChain: face detection and 512-dimensional embedding extraction with InsightFace, followed by cosine-similarity matching.

## Setup

Create and activate a Python virtual environment, then install dependencies:

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in any service credentials needed by the wider application. The `.env` file and virtual environments are deliberately excluded from version control.

## Face detection

`FaceDetector` loads InsightFace's `buffalo_l` model using the CPU provider. It detects all faces in an image, selects the largest as the primary face, and returns its bounding box, confidence score, face count, and L2-normalized embedding.

```python
from src.face.detector import FaceDetector

result = FaceDetector().process_image("path/to/photo.jpg")
embedding = result["embedding"]
```

The InsightFace model downloads on its first use.

## Cosine matching

`FaceMatcher` compares equal-shaped normalized embeddings via their dot product, which is cosine similarity, and reports whether the score meets the configured threshold (default: `0.5`).

```python
from src.face.matcher import FaceMatcher

matcher = FaceMatcher(threshold=0.5)
similarity = matcher.compute_similarity(embedding_a, embedding_b)
is_same_person = matcher.is_match(embedding_a, embedding_b)
```

## Repository layout

- `src/face/detector.py` — detection and normalized embedding extraction.
- `src/face/matcher.py` — cosine similarity and threshold-based matching.
- `tests/test_face.py` — manual detector smoke test.
- `data/` — local input, candidate, and result data; image contents are ignored by Git.
