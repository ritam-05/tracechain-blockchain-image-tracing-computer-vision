import os
import sys
import json
from web3 import Web3
import solcx

# Ensure root directory is accessible for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def compile_contract():
    print("Installing Solidity compiler (v0.8.19)...")
    solcx.install_solc('0.8.19')
    
    print("Compiling ContentRegistry.sol...")
    contract_path = os.path.join("contracts", "ContentRegistry.sol")
    with open(contract_path, "r") as f:
        contract_source = f.read()

    compiled_sol = solcx.compile_source(
        contract_source,
        output_values=['abi', 'bin'],
        solc_version='0.8.19'
    )

    # Extract the compiled contract data
    contract_id, contract_interface = compiled_sol.popitem()
    
    # Save the ABI (Application Binary Interface) so our main app knows how to talk to it
    os.makedirs("abi", exist_ok=True)
    abi_path = os.path.join("abi", "ContentRegistry.json")
    with open(abi_path, "w") as f:
        json.dump(contract_interface['abi'], f, indent=2)
        
    return contract_interface['abi'], contract_interface['bin']

def deploy():
    # 1. Connect to Sepolia
    w3 = Web3(Web3.HTTPProvider(Config.WEB3_PROVIDER_URI))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Alchemy RPC. Check WEB3_PROVIDER_URI in .env")
        
    print(f"Connected to Sepolia. Current Block: {w3.eth.block_number}")

    # 2. Setup Wallet
    account = w3.eth.account.from_key(Config.PRIVATE_KEY)
    print(f"Deploying from address: {account.address}")
    
    balance = w3.eth.get_balance(account.address)
    if balance == 0:
        raise ValueError("Wallet has 0 Sepolia ETH! Please use a faucet to get test ETH.")
    else:
        print(f"Wallet balance: {w3.from_wei(balance, 'ether')} ETH")

    # 3. Compile
    abi, bytecode = compile_contract()
    print("✓ Compilation successful.")

    # 4. Create Contract Object
    ContentRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)

    # 5. Build Transaction
    print("\nBuilding deployment transaction...")
    nonce = w3.eth.get_transaction_count(account.address)
    
    # EIP-1559 gas settings for Sepolia
    latest_block = w3.eth.get_block('latest')
    base_fee = latest_block['baseFeePerGas']
    max_priority_fee = w3.to_wei(2, 'gwei')
    max_fee = base_fee + max_priority_fee

    transaction = ContentRegistry.constructor().build_transaction({
        'chainId': 11155111, # Standard Sepolia Chain ID
        'gas': 2000000,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee,
        'nonce': nonce,
    })

    # 6. Sign and Send
    print("Signing and broadcasting to Sepolia (this takes ~15 seconds)...")
    # web3.py v6 uses rawTransaction for the signed output
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=Config.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # 7. Wait for network confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    
    print("\n✓ SUCCESS: Smart Contract Deployed!")
    print(f"  Contract Address : {contract_address}")
    print(f"  Transaction Hash : {tx_receipt.transactionHash.hex()}")
    print(f"  View on Etherscan: https://sepolia.etherscan.io/address/{contract_address}")
    
    print("\n⚠️ ACTION REQUIRED ⚠️")
    print("Open your .env file and add this exact line at the bottom:")
    print(f'CONTRACT_ADDRESS="{contract_address}"')

if __name__ == "__main__":
    deploy()