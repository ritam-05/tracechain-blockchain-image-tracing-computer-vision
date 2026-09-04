import os
from src.face.detector import FaceDetector
from src.face.matcher import FaceMatcher
from src.search.lens import LensSearch
from src.content.extractor import ContentExtractor
from src.content.canonicalizer import ContentCanonicalizer
from src.crypto.hashing import Hasher
from src.blockchain.ethereum import BlockchainRegistry

class TraceChainPipeline:
    """Orchestrates the end-to-end TraceChain verification process."""

    def __init__(self):
        print("[System] Initializing AI Models & Blockchain connections...")
        self.detector = FaceDetector()
        self.matcher = FaceMatcher(threshold=0.5)
        self.searcher = LensSearch()
        self.extractor = ContentExtractor()
        self.blockchain = BlockchainRegistry()

    def process_image(self, image_path: str):
        print(f"\n" + "="*50)
        print(f"🕵️  TRACECHAIN PIPELINE STARTED")
        print(f"Target: {image_path}")
        print("="*50)

        # 1. Initial Face Scan
        print("\n[1/6] Scanning input image for facial embeddings...")
        query_result = self.detector.process_image(image_path)
        query_embedding = query_result["embedding"]
        print("  ✓ Face detected and embedded.")

        # 2. Web Search
        print("\n[2/6] Querying Google Lens via SerpApi...")
        search_results = self.searcher.search(image_path)
        candidates = self.searcher.extract_candidates(search_results, limit=5)
        print(f"  ✓ Found {len(candidates)} visual matches.")

        # 3. Download Candidates
        print("\n[3/6] Downloading candidate images for verification...")
        downloaded_candidates = self.searcher.download_candidates(candidates)

        # 4. AI Face Matching
        print("\n[4/6] Cross-referencing web candidates with target embedding...")
        scored_candidates = self.matcher.match_candidates(
            query_embedding, downloaded_candidates, self.detector
        )
        best_match = self.matcher.select_best_match(scored_candidates)

        if not best_match:
            print("\n❌ VERIFICATION FAILED: No authentic match found online.")
            return

        print(f"  ✓ Authentic match found! (Similarity: {best_match['similarity']:.4f})")

        # 5. Extract & Canonicalize
        print("\n[5/6] Extracting metadata & generating cryptographic fingerprint...")
        metadata = self.extractor.extract_metadata(best_match)
        image_hash = Hasher.hash_file(best_match["local_path"])
        canonical_str = ContentCanonicalizer.canonicalize(metadata, image_hash)
        final_fingerprint = Hasher.hash_string(canonical_str)
        
        print(f"  Title      : {metadata['title']}")
        print(f"  Source     : {metadata['url']}")
        print(f"  Fingerprint: 0x{final_fingerprint}")

        # 6. Blockchain Registration
        print("\n[6/6] Interacting with Ethereum Sepolia Blockchain...")
        is_registered = self.blockchain.verify_content(final_fingerprint)

        if is_registered:
            print("\n🟢 VERIFIED: This content is already secured on the blockchain!")
            print(f"   Smart Contract: {os.getenv('CONTRACT_ADDRESS')}")
        else:
            print("  -> Fingerprint is new. Registering on-chain...")
            tx_hash = self.blockchain.register_content(final_fingerprint, metadata["url"])
            if tx_hash:
                print(f"\n🟢 SUCCESS: Content registered permanently!")
                print(f"   Transaction Hash: {tx_hash}")
                print(f"   View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}")

        print("="*50 + "\n")