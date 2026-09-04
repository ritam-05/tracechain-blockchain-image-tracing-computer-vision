# TraceChain — User Manual

This manual explains how to install, configure, run, and verify TraceChain on a new computer.

The instructions assume that the user has little or no prior blockchain experience.

---

# 1. What You Need

Before starting, make sure the computer has:

* Python 3.9+
* Git
* Internet access
* A SerpApi account/API key
* An Alchemy account/API key
* A MetaMask wallet
* Sepolia test ETH
* The deployed TraceChain smart-contract address
* The TraceChain repository

The application itself runs from the command line.

No website is required.

---

# 2. Clone the Repository

Open Command Prompt, PowerShell, Terminal, or another terminal.

Clone the GitHub repository:

```bash
git clone <your-repository-url>
```

Example:

```bash
git clone https://github.com/username/tracechain.git
```

Enter the project:

```bash
cd tracechain
```

Verify that the repository contains files such as:

```text
README.md
USER_MANUAL.md
main.py
requirements.txt
src/
contracts/
abi/
data/
```

---

# 3. Install Python

Check whether Python is installed:

```bash
python --version
```

You should see:

```text
Python 3.9
```

or a newer version.

If `python` does not work, try:

```bash
python3 --version
```

---

# 4. Install Git

Check:

```bash
git --version
```

If Git is installed, a version number will be displayed.

---

# 5. Create a Virtual Environment

From the TraceChain directory:

```bash
python -m venv venv
```

This creates an isolated Python environment.

The directory will look like:

```text
tracechain/
├── venv/
├── main.py
└── ...
```

---

# 6. Activate the Virtual Environment

## Windows Command Prompt

```cmd
venv\Scripts\activate
```

## Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

## macOS/Linux

```bash
source venv/bin/activate
```

You should now see something similar to:

```text
(venv)
```

at the beginning of the terminal prompt.

---

# 7. Upgrade pip

Run:

```bash
python -m pip install --upgrade pip
```

Wait for the command to finish.

---

# 8. Install TraceChain Dependencies

Run:

```bash
pip install -r requirements.txt
```

This installs the libraries required by TraceChain.

The installation may take several minutes because InsightFace and its machine-learning dependencies can be relatively large.

---

# 9. Configure SerpApi

TraceChain uses SerpApi to perform the Google Lens search.

Create or access your SerpApi account and obtain an API key.

The key should look like a long alphanumeric string.

Create a file named:

```text
.env
```

in the root of the TraceChain project.

Add:

```env
SERPAPI_KEY="your_actual_serpapi_key"
```

Replace the placeholder with your real key.

---

# 10. Configure Alchemy

TraceChain uses Alchemy as the RPC provider for Ethereum Sepolia.

Create an Alchemy account and create an application configured for Ethereum Sepolia.

Copy the Sepolia RPC endpoint/API key.

Add the following to `.env`:

```env
WEB3_PROVIDER_URI="https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY"
```

Replace:

```text
YOUR_ALCHEMY_API_KEY
```

with your actual Alchemy API key.

---

# 11. Understand the Blockchain Setup

You do not need to run your own blockchain.

TraceChain uses:

```text
Ethereum Sepolia
```

Sepolia is a public Ethereum test network.

The architecture is:

```text
TraceChain
    ↓
Web3.py
    ↓
Alchemy
    ↓
Ethereum Sepolia
    ↓
ContentRegistry
```

The application communicates with Ethereum through the Alchemy RPC endpoint.

---

# 12. Create a Dedicated MetaMask Wallet

Install MetaMask if it is not already installed.

Create a separate wallet for the hackathon.

Do not use a wallet containing valuable cryptocurrency.

This wallet will only be used for Sepolia testnet transactions.

---

# 13. Switch MetaMask to Sepolia

Open MetaMask.

Select the Ethereum network selector.

Choose:

```text
Sepolia
```

Your wallet is now operating on the Sepolia test network.

---

# 14. Obtain the Wallet Private Key

TraceChain needs a private key because Python must sign blockchain transactions.

In MetaMask, use the account's export/private-key functionality.

Copy the private key.

Add it to `.env`:

```env
PRIVATE_KEY="your_wallet_private_key"
```

### IMPORTANT

Never:

```text
post the private key
commit it to GitHub
send it to another person
put it into main.py
include it in screenshots
```

Use a disposable hackathon wallet.

---

# 15. Obtain Sepolia Test ETH

The wallet needs Sepolia test ETH to submit transactions.

Use an appropriate Sepolia testnet faucet and send test ETH to your MetaMask Sepolia address.

After receiving the funds, confirm that the Sepolia balance is visible in MetaMask.

The ETH used here has no mainnet monetary value.

---

# 16. Configure the Smart Contract

TraceChain uses:

```text
ContentRegistry
```

The contract must be deployed to Ethereum Sepolia.

After deployment, you receive a contract address.

Example:

```text
0x1234567890abcdef1234567890abcdef12345678
```

Add it to `.env`:

```env
CONTRACT_ADDRESS="0x1234567890abcdef1234567890abcdef12345678"
```

Use the actual deployed contract address.

---

# 17. Complete `.env`

At this point, your `.env` should contain:

```env
SERPAPI_KEY="your_actual_serpapi_key"

WEB3_PROVIDER_URI="https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY"

PRIVATE_KEY="your_wallet_private_key"

CONTRACT_ADDRESS="your_deployed_contract_address"
```

Do not commit this file.

---

# 18. Check `.gitignore`

Make sure `.gitignore` contains:

```text
.env
venv/
__pycache__/
*.pyc
output/
data/candidates/
```

The most important entry is:

```text
.env
```

This prevents your private credentials from being uploaded to GitHub.

---

# 19. Check the Contract ABI

The project must contain:

```text
abi/ContentRegistry.json
```

The ABI tells Web3.py how to communicate with the Solidity contract.

It must correspond to the exact deployed `ContentRegistry` contract.

The project should therefore look like:

```text
tracechain/
│
├── abi/
│   └── ContentRegistry.json
│
├── contracts/
│   └── ContentRegistry.sol
```

---

# 20. Prepare an Input Image

Create or use:

```text
data/input/
```

Place your image inside it.

Example:

```text
data/input/test.webp
```

Other supported formats may include:

```text
.jpg
.jpeg
.png
.webp
```

The image should contain a clearly visible face.

For the best demonstration:

* Use a relatively high-resolution image.
* Avoid extreme blur.
* Avoid heavy face obstruction.
* Use an image with public web presence if you want Google Lens to find related results.

---

# 21. Run the Pipeline

From the root of the project:

```bash
python main.py data/input/test.webp
```

Replace the filename with your actual image.

For example:

```bash
python main.py data/input/example.jpg
```

---

# 22. Stage 1 — Face Detection

TraceChain first loads the image and detects faces.

Expected output:

```text
[1] FACE DETECTION

✓ Input image loaded
✓ Face detected
```

If no face is detected:

```text
✗ No face detected
```

Try another image.

---

# 23. Stage 2 — Face Embedding

InsightFace generates a numerical embedding for the detected face.

Expected:

```text
[2] FACE EMBEDDING

✓ Facial embedding generated
```

The embedding is used later to compare the target face with candidate faces.

---

# 24. Stage 3 — Google Lens Search

The input image is sent to Google Lens through SerpApi.

Expected:

```text
[3] WEB SEARCH

✓ Search completed
✓ Candidates discovered
```

The results are dynamically obtained.

The application does not select a hardcoded final URL.

---

# 25. Stage 4 — Candidate Processing

TraceChain downloads accessible candidate images.

You may see:

```text
Candidate 1 downloaded
Candidate 2 downloaded
Candidate 3 skipped
Candidate 4 downloaded
```

A candidate may be skipped because the source website prevents automated image access.

This does not necessarily indicate a problem with the pipeline.

---

# 26. Stage 5 — Face Matching

Each usable candidate is processed using InsightFace.

Example:

```text
[4] FACE MATCHING

Candidate 1 similarity: 0.31
Candidate 2 similarity: 0.64
Candidate 3 similarity: 0.88

✓ Best candidate selected

Similarity: 0.88
```

The exact values depend on the input image and search results.

---

# 27. Stage 6 — Matching Content

TraceChain displays the strongest candidate.

Example:

```text
MATCH FOUND

Title:
Example Post

Source:
example.com

URL:
https://example.com/post/123

Similarity:
0.88
```

The source URL should come from the live search response.

---

# 28. Stage 7 — Content Fingerprinting

The matching content is converted into a deterministic representation.

TraceChain calculates:

```text
Image SHA-256
       ↓
Canonical metadata
       ↓
Final SHA-256 fingerprint
```

Example:

```text
[6] CONTENT FINGERPRINT

✓ Fingerprint generated

a6fb136ad91503...
```

---

# 29. Stage 8 — Blockchain Registration

TraceChain connects to Ethereum Sepolia.

Expected:

```text
[7] BLOCKCHAIN

Network: Ethereum Sepolia

✓ RPC connection successful
✓ Contract loaded
```

The application checks whether the fingerprint has already been registered.

If it is new:

```text
✓ Fingerprint not previously registered
✓ Transaction submitted
```

---

# 30. Stage 9 — Transaction Confirmation

The application waits for the transaction to be confirmed.

Expected:

```text
✓ Transaction confirmed

Transaction Hash:
0x...

Contract:
0x...
```

The transaction hash is the unique identifier of the blockchain transaction.

---

# 31. Stage 10 — Blockchain Verification

TraceChain then queries the smart contract.

Expected:

```text
[8] BLOCKCHAIN VERIFICATION

✓ Fingerprint found on-chain

CONTENT VERIFIED
```

The application has now completed the full pipeline.

---

# 32. Verify the Transaction Independently

The transaction hash can be checked using the Sepolia blockchain explorer.

Copy the transaction hash printed by TraceChain.

Search for it on the Sepolia explorer.

Verify that:

```text
Transaction status = successful
Network = Sepolia
Contract = ContentRegistry
```

This provides an independent blockchain-level verification of the transaction.

---

# 33. Inspect the Output Transcript

TraceChain generates a transcript under:

```text
output/
```

Example:

```text
output/run_test.txt
```

Open the file to inspect the complete execution record.

It may contain:

```text
Input image
Face detection
Search results
Candidate scores
Selected URL
Image hash
Content fingerprint
Contract address
Transaction hash
Verification result
```

---

# 34. Testing Tamper Detection

The most important blockchain demonstration is to show that modifying the content changes its fingerprint.

Start with the original discovered content.

Suppose:

```text
Original fingerprint:
A6FB136...
```

The fingerprint is registered on-chain.

Now modify the local content.

For example:

```text
Original image
     ↓
Crop / modify / alter
     ↓
Modified image
```

Calculate the new fingerprint.

Suppose:

```text
Modified fingerprint:
73AC917...
```

The blockchain still contains:

```text
A6FB136...
```

Therefore:

```text
73AC917...
      ≠
A6FB136...
```

TraceChain reports:

```text
✗ VERIFICATION FAILED
CONTENT HAS CHANGED
```

This is the primary demonstration of tamper detection.

---

# 35. If the Fingerprint Already Exists

If you run the same input again, the content may already be registered.

TraceChain can report:

```text
✓ Fingerprint already registered

Existing blockchain record found.
```

This is expected.

It means the same fingerprint was already recorded on-chain.

---

# 36. Common Error: No Face Detected

Message:

```text
No face detected
```

Try:

* A higher-resolution image
* A front-facing image
* An image without heavy obstruction
* A different input

---

# 37. Common Error: No Search Results

Possible reasons:

* The image has little web presence.
* Google Lens did not find useful visual matches.
* Search API quota is exhausted.
* The API key is invalid.

Try another public test image.

---

# 38. Common Error: No Matching Face

Google Lens may find visually related images that do not contain the same face.

For example:

```text
Lens Result
     ↓
Similar clothing
Similar scene
Similar composition
     ↓
Different person
```

TraceChain should reject such results when the face similarity is below the configured threshold.

---

# 39. Common Error: Candidate Download Failed

Some websites block automated image downloads.

You may see:

```text
Candidate skipped
```

This is expected for some websites.

The pipeline should continue processing other candidates.

---

# 40. Common Error: Invalid SerpApi Key

Check:

```env
SERPAPI_KEY="..."
```

Make sure:

* The key is correct.
* There are no accidental characters.
* `.env` is located in the project root.
* The virtual environment is active.

---

# 41. Common Error: Blockchain Connection Failed

Check:

```env
WEB3_PROVIDER_URI="..."
```

Make sure:

* Alchemy key is correct.
* The URL points to Sepolia.
* Internet access is available.
* The Alchemy application is active.

---

# 42. Common Error: Insufficient Funds

If the blockchain transaction fails because of insufficient funds:

1. Open MetaMask.
2. Switch to Sepolia.
3. Copy the wallet address.
4. Obtain additional Sepolia test ETH from a faucet.
5. Wait for the balance to update.
6. Run TraceChain again.

---

# 43. Common Error: Invalid Contract Address

Check:

```env
CONTRACT_ADDRESS="..."
```

Confirm that:

* It starts with `0x`.
* It is the deployed `ContentRegistry` address.
* It was deployed on Sepolia.
* The ABI corresponds to that deployment.

---

# 44. Common Error: ABI Mismatch

If Python reports that a contract function does not exist, the ABI may not correspond to the deployed contract.

Replace:

```text
abi/ContentRegistry.json
```

with the ABI generated from the exact Solidity contract deployment.

---

# 45. Security Checklist

Before pushing the project to GitHub, verify:

```text
[ ] .env is in .gitignore
[ ] Private key is not in source code
[ ] API keys are not in source code
[ ] Wallet seed phrase is not stored anywhere
[ ] No credentials appear in README screenshots
[ ] No credentials appear in output logs
```

You can check Git's tracked files with:

```bash
git status
```

Make sure `.env` is not listed as a file that will be committed.

---

# 46. Complete First-Time Setup

For a completely new computer, the process is:

```text
1. Install Python
        ↓
2. Install Git
        ↓
3. Clone TraceChain
        ↓
4. cd tracechain
        ↓
5. Create virtual environment
        ↓
6. Activate virtual environment
        ↓
7. pip install -r requirements.txt
        ↓
8. Create .env
        ↓
9. Add SerpApi key
        ↓
10. Add Alchemy RPC
        ↓
11. Add wallet private key
        ↓
12. Add contract address
        ↓
13. Verify ABI
        ↓
14. Add input image
        ↓
15. Run main.py
        ↓
16. Verify blockchain transaction
```

---

# 47. Quick Run

If the computer has already been configured:

```bash
cd tracechain
```

Activate the environment:

```bash
venv\Scripts\activate
```

Run:

```bash
python main.py data/input/test.webp
```

The expected final result is:

```text
✓ Face detected
✓ Web search completed
✓ Matching content found
✓ Content fingerprint generated
✓ Blockchain transaction confirmed
✓ Fingerprint verified on-chain
```

---

# 48. End-to-End Success Criteria

A successful TraceChain run must demonstrate all of the following:

```text
✓ A face was detected

✓ A face embedding was generated

✓ A genuine web/reverse-image search was performed

✓ Candidate web content was dynamically discovered

✓ At least one candidate was facially matched

✓ The discovered source URL came from the search result

✓ A deterministic content fingerprint was generated

✓ The fingerprint was registered on Ethereum Sepolia

✓ A real blockchain transaction was confirmed

✓ The fingerprint was queried from the smart contract

✓ The content successfully matched the on-chain fingerprint

✓ A modified version fails verification
```

If all of these conditions are satisfied, the complete TraceChain pipeline is operational.
