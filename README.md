# TraceChain

**AI-Powered Web Content Discovery and Blockchain Verification**

TraceChain is an end-to-end AI and blockchain pipeline that takes a face-containing image as input, searches the web for visually matching content, verifies candidate results using facial recognition, and creates a tamper-evident blockchain record of the discovered content.

The project combines **computer vision, reverse-image search, cryptographic hashing, and blockchain technology** into a single automated pipeline.

---

## 1. Problem

Online images and social-media content can be difficult to trace back to their original sources.

A piece of visual content may be:

* Reposted across multiple platforms
* Modified after publication
* Taken out of context
* Difficult to trace to its original source
* Presented without reliable provenance

Traditional reverse-image search can help locate visually similar content, but it does not provide a cryptographically verifiable record of what was discovered.

TraceChain addresses this by combining web discovery with blockchain-backed content fingerprinting.

---

## 2. Solution

TraceChain follows this pipeline:

```text
                INPUT IMAGE
                     │
                     ▼
          ┌─────────────────────┐
          │ Face Detection      │
          │ + Face Embedding    │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Google Lens Search  │
          │ via SerpApi         │
          └──────────┬──────────┘
                     │
                     ▼
             Candidate Results
                     │
                     ▼
          Candidate Image Download
                     │
                     ▼
          ┌─────────────────────┐
          │ Face Matching       │
          │ Cosine Similarity   │
          └──────────┬──────────┘
                     │
                     ▼
              Matching Content
                     │
                     ▼
           Metadata Extraction
                     │
                     ▼
          Deterministic Canonicalization
                     │
                     ▼
                SHA-256
                     │
                     ▼
          ┌─────────────────────┐
          │ Ethereum Sepolia    │
          │ ContentRegistry     │
          └──────────┬──────────┘
                     │
                     ▼
             Blockchain Record
                     │
                     ▼
               Re-verification
```

---

## 3. Core Features

### Face Detection & Recognition

TraceChain uses **InsightFace** and its `buffalo_l` model package to:

1. Detect faces in the input image.
2. Generate facial embeddings.
3. Compare the target face against faces found in candidate images.

---

### Genuine Web Search

The input image is submitted to **Google Lens through SerpApi**.

The search is performed dynamically at runtime.

The application does not contain a hardcoded final social-media or web result.

The search process is:

```text
Input Image
     ↓
SerpApi
     ↓
Google Lens
     ↓
Visual Search Results
     ↓
Candidate URLs + Images
```

---

### Face-Based Candidate Verification

Google Lens results are treated as candidates rather than automatically accepted as matches.

Each accessible candidate image is processed using the same face-recognition pipeline.

Cosine similarity is then used to compare:

```text
Target Face Embedding
          vs
Candidate Face Embedding
```

The highest qualifying result is selected as the matching candidate.

---

### Deterministic Content Fingerprinting

After a matching result is discovered, TraceChain creates a structured representation of the content.

The record can contain:

```text
Source URL
Platform
Title
Text/metadata
Image SHA-256
```

The record is serialized deterministically and hashed using SHA-256.

This produces the final content fingerprint.

```text
Content Metadata
      +
Image Fingerprint
      ↓
Canonical JSON
      ↓
SHA-256
      ↓
Content Fingerprint
```

---

## 4. Blockchain Verification

TraceChain uses the **Ethereum Sepolia testnet**.

The blockchain architecture is:

```text
Python
  │
  ▼
Web3.py
  │
  ▼
Alchemy RPC
  │
  ▼
Ethereum Sepolia
  │
  ▼
ContentRegistry
```

The blockchain stores the content fingerprint rather than the complete image.

A record contains information such as:

```text
Content Hash
Source URL
Timestamp
Submitting Address
```

This provides an externally verifiable record of the fingerprint.

---

## 5. Why Blockchain?

The blockchain is used as a tamper-evident reference point.

Suppose the original content produces:

```text
SHA-256:
A6FB136AD91503...
```

TraceChain registers that fingerprint on-chain.

If the content is later modified:

```text
Modified Content
      ↓
SHA-256
      ↓
73AC917BD712...
```

The fingerprints no longer match:

```text
Blockchain:
A6FB136AD91503...

Current:
73AC917BD712...

✗ VERIFICATION FAILED
```

If the content remains unchanged:

```text
Blockchain:
A6FB136AD91503...

Current:
A6FB136AD91503...

✓ CONTENT VERIFIED
```

---

## 6. Smart Contract

TraceChain uses a Solidity smart contract named:

```text
ContentRegistry
```

The contract provides functionality for:

* Registering content fingerprints
* Storing source URLs
* Recording timestamps
* Checking whether a fingerprint already exists
* Emitting registration events

The contract intentionally stores only compact verification information.

The original image is not stored directly on Ethereum.

---

## 7. Technology Stack

| Component            | Technology        |
| -------------------- | ----------------- |
| Programming Language | Python            |
| Face Recognition     | InsightFace       |
| Face Detection       | InsightFace       |
| Image Processing     | OpenCV / Pillow   |
| Web Search           | Google Lens       |
| Search API           | SerpApi           |
| Similarity           | Cosine Similarity |
| Cryptography         | SHA-256           |
| Smart Contract       | Solidity          |
| Blockchain           | Ethereum Sepolia  |
| Blockchain Interface | Web3.py           |
| RPC Provider         | Alchemy           |
| Wallet               | MetaMask          |
| Interface            | CLI               |

---

## 8. Repository Structure

```text
tracechain/
│
├── README.md
├── USER_MANUAL.md
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
├── config.py
│
├── src/
│   ├── __init__.py
│   │
│   ├── face/
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── matcher.py
│   │
│   ├── search/
│   │   ├── __init__.py
│   │   └── lens.py
│   │
│   ├── content/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   └── canonicalizer.py
│   │
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── hashing.py
│   │
│   ├── blockchain/
│   │   ├── __init__.py
│   │   └── ethereum.py
│   │
│   └── pipeline.py
│
├── contracts/
│   └── ContentRegistry.sol
│
├── scripts/
│   ├── deploy.py
│   └── verify_contract.py
│
├── abi/
│   └── ContentRegistry.json
│
├── data/
│   ├── input/
│   ├── candidates/
│   └── results/
│
├── output/
│
└── tests/
    ├── test_face.py
    ├── test_hashing.py
    └── test_blockchain.py
```

---

## 9. Environment Variables

TraceChain uses environment variables for external credentials.

Required variables:

```env
SERPAPI_KEY="your_serpapi_key"

WEB3_PROVIDER_URI="https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY"

PRIVATE_KEY="your_wallet_private_key"

CONTRACT_ADDRESS="your_deployed_contract_address"
```

### Security

`.env` must never be committed to GitHub.

The repository should contain:

```text
.env.example
```

but not the real `.env`.

The private key should belong to a dedicated development wallet containing only testnet funds.

---

## 10. Running the Project

After installation and configuration:

```bash
python main.py data/input/test.webp
```

Example:

```bash
python main.py data/input/example.jpg
```

The application executes the complete pipeline automatically.

---

## 11. Example CLI Output

```text
==================================================
                  TRACECHAIN
==================================================

[1] FACE DETECTION
✓ Face detected

[2] FACE EMBEDDING
✓ Facial embedding generated

[3] WEB SEARCH
✓ Google Lens search completed
✓ 17 candidates discovered

[4] FACE MATCHING
Candidate 1: 0.34
Candidate 2: 0.71
Candidate 3: 0.89

✓ Matching content identified
Similarity: 0.89

[5] CONTENT EXTRACTION
✓ Metadata extracted

[6] CONTENT FINGERPRINT
✓ SHA-256 generated

Fingerprint:
a6fb136ad91503...

[7] BLOCKCHAIN REGISTRATION
Network: Ethereum Sepolia
✓ Transaction confirmed

Transaction:
0x...

[8] BLOCKCHAIN VERIFICATION
✓ Fingerprint found on-chain

==================================================
                 CONTENT VERIFIED
==================================================
```

---

## 12. Output

Each execution can generate a transcript in:

```text
output/
```

Example:

```text
output/run_test.txt
```

The transcript records important execution information such as:

* Input image
* Search results
* Candidate count
* Similarity scores
* Selected source
* Source URL
* Image hash
* Content fingerprint
* Blockchain network
* Contract address
* Transaction hash
* Verification result

---

## 13. Tamper Demonstration

TraceChain supports demonstrating what happens when registered content changes.

### Original

```text
Content
  ↓
SHA-256
  ↓
A6FB136...
  ↓
Ethereum
```

### Modified

```text
Modified Content
  ↓
SHA-256
  ↓
73AC917...
```

Comparison:

```text
On-chain fingerprint:
A6FB136...

Current fingerprint:
73AC917...

✗ VERIFICATION FAILED
```

This demonstrates the tamper-evident property of the system.

---

## 14. What the Blockchain Proves

Blockchain verification should not be interpreted as proof that the content itself is true.

The blockchain proves that a particular fingerprint was registered at a particular point in the blockchain's history.

Therefore:

```text
Blockchain
     ≠
Truth Detector
```

Instead:

```text
Blockchain
     =
Tamper-Evident Reference
```

TraceChain combines this with web discovery and facial matching to create a provenance-oriented workflow.

---

## 15. Privacy and Responsible Use

Facial recognition and web-based identity discovery can have significant privacy implications.

TraceChain should be demonstrated using:

* Consented images
* Publicly available test images
* Images owned by the developers
* Appropriate public/educational datasets

The system should not be used to track or identify private individuals without appropriate authorization.

The project is intended as a technical demonstration of content discovery and provenance verification.

---

## 16. Known Limitations

### Search limitations

Google Lens results depend on what is indexed and returned by the search provider.

### Social media restrictions

Some platforms restrict automated access to images, pages, or metadata.

### Candidate availability

Not every search result provides a downloadable image.

### Face recognition accuracy

Similarity scores are affected by:

* Image quality
* Lighting
* Pose
* Occlusion
* Resolution
* Facial expression

A similarity score should not be treated as absolute proof of identity.

### Metadata changes

Web pages and metadata can change after discovery.

TraceChain verifies the fingerprint of the recorded representation rather than guaranteeing that the source itself will remain unchanged.

### Blockchain network

The current implementation uses Ethereum Sepolia for demonstration and testing.

It is not intended as a production deployment.

---

## 17. Future Improvements

Possible future improvements include:

* Multiple reverse-image search providers
* IPFS-based content storage
* Additional provenance metadata
* Confidence calibration
* Multi-face tracking
* More social-media integrations
* Production blockchain deployment
* Decentralized storage
* Automated provenance reports
* Browser-based visualization

---

## 18. Hackathon Demonstration

The recommended demonstration consists of two scenarios.

### Scenario 1 — Successful verification

```text
Input Image
     ↓
Google Lens
     ↓
Real Web Result
     ↓
Face Match
     ↓
SHA-256
     ↓
Ethereum Transaction
     ↓
✓ VERIFIED
```

### Scenario 2 — Tampered content

```text
Registered Content
     ↓
Modify Image
     ↓
Recalculate SHA-256
     ↓
Compare with Blockchain
     ↓
✗ VERIFICATION FAILED
```

The second demonstration shows why the blockchain component exists rather than treating it as an unrelated technology added to the project.

---

## 19. Summary

TraceChain combines four technologies into one end-to-end pipeline:

```text
Computer Vision
      +
Web Search
      +
Cryptographic Fingerprinting
      +
Blockchain
```

The result is a system capable of discovering web content associated with a face, independently matching candidate content using facial embeddings, generating a deterministic fingerprint, registering that fingerprint on Ethereum Sepolia, and verifying whether the recorded content has subsequently changed.
