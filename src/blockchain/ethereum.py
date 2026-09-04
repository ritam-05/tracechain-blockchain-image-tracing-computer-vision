import os
import sys
import json
from web3 import Web3

# Ensure root directory is accessible for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import Config

class BlockchainRegistry:
    """Handles interactions with the deployed ContentRegistry smart contract."""

    def __init__(self):
        # 1. Connect to Sepolia via Alchemy
        self.w3 = Web3(Web3.HTTPProvider(Config.WEB3_PROVIDER_URI))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Alchemy RPC.")
        
        self.account = self.w3.eth.account.from_key(Config.PRIVATE_KEY)
        
        # 2. Load ABI from the Remix deployment
        abi_path = os.path.join("abi", "ContentRegistry.json")
        if not os.path.exists(abi_path):
            raise FileNotFoundError(f"ABI file missing at {abi_path}. Please copy it from Remix.")
        
        with open(abi_path, "r") as f:
            abi = json.load(f)
            
        # 3. Connect to the specific contract address
        contract_address = os.getenv("CONTRACT_ADDRESS")
        if not contract_address:
            raise ValueError("CONTRACT_ADDRESS is missing from the .env file.")
            
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)

    def verify_content(self, fingerprint_hex: str) -> bool:
        """Calls the smart contract to check if a fingerprint exists (Free & Instant)."""
        # Ensure correct hex formatting for Web3 bytes32
        if not fingerprint_hex.startswith("0x"):
            fingerprint_hex = "0x" + fingerprint_hex
            
        fingerprint_bytes = self.w3.to_bytes(hexstr=fingerprint_hex)
        
        # .call() reads data without spending gas
        return self.contract.functions.isRegistered(fingerprint_bytes).call()

    def register_content(self, fingerprint_hex: str, source_url: str) -> str:
        """Sends a transaction to register a new fingerprint (Costs Gas & Takes ~15s)."""
        if not fingerprint_hex.startswith("0x"):
            fingerprint_hex = "0x" + fingerprint_hex
            
        fingerprint_bytes = self.w3.to_bytes(hexstr=fingerprint_hex)

        # Safety check to prevent wasting gas on duplicates
        if self.verify_content(fingerprint_hex):
            print("  -> Fingerprint is already registered! Skipping transaction.")
            return None

        print("  -> Building blockchain transaction...")
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        
        # Modern EIP-1559 gas fee estimation for Sepolia
        latest_block = self.w3.eth.get_block('latest')
        base_fee = latest_block['baseFeePerGas']
        max_priority_fee = self.w3.to_wei(2, 'gwei')
        
        tx = self.contract.functions.registerContent(
            fingerprint_bytes, 
            source_url
        ).build_transaction({
            'chainId': 11155111,
            'gas': 300000,
            'maxFeePerGas': base_fee + max_priority_fee,
            'maxPriorityFeePerGas': max_priority_fee,
            'nonce': nonce,
        })

        print("  -> Signing and broadcasting to Sepolia... (Please wait ~15 seconds)")
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=Config.PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for the blockchain network to mine the block
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()

if __name__ == "__main__":
    print("Testing Web3 Contract Interaction...\n")
    try:
        registry = BlockchainRegistry()
        print(f"✓ Connected to Contract: {os.getenv('CONTRACT_ADDRESS')}")
        
        # Use a dummy 32-byte hash for the test
        test_fingerprint = "0x" + "1" * 64
        test_url = "https://example.com/test-tracechain"
        
        print("\n1. Checking if test fingerprint is registered...")
        is_reg = registry.verify_content(test_fingerprint)
        print(f"   Registered? {is_reg}")
        
        if not is_reg:
            print("\n2. Registering test fingerprint...")
            tx_hash = registry.register_content(test_fingerprint, test_url)
            print(f"✓ Registration Successful! TX Hash: {tx_hash}")
            
            print("\n3. Verifying registration...")
            print(f"   Registered? {registry.verify_content(test_fingerprint)}")
            
    except Exception as e:
        print(f"✗ ERROR: {e}")