import os
import logging
from logging.handlers import RotatingFileHandler
import nacl.utils
from nacl.public import PrivateKey, SealedBox
from nacl.encoding import Base64Encoder
from web3 import Web3
# The import of geth_poa_middleware from web3.middleware.geth_poa is failing due to version mismatch.
# We will import geth_poa_middleware from web3.middleware instead.
from web3.middleware.geth_poa import geth_poa_middleware
import json
import subprocess

# Configure logging
logger = logging.getLogger("backend_integration")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = "backend_integration.log"
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
handler.setFormatter(log_formatter)
logger.addHandler(handler)

# BTFS CLI command (assumes btfs is installed and in PATH)
BTFS_CLI = "btfs"

# BTTC smart contract info (to be configured)
BTTC_RPC_URL = os.getenv("BTTC_RPC_URL", "https://rpc-testnet.bittorrentchain.io")
BTTC_CONTRACT_ADDRESS = os.getenv("BTTC_CONTRACT_ADDRESS")
BTTC_CONTRACT_ABI_PATH = os.getenv("BTTC_CONTRACT_ABI_PATH", "bttc_cid_mapping_abi.json")

# Web3 setup
w3 = Web3(Web3.HTTPProvider(BTTC_RPC_URL))
# Add middleware for PoA chains if needed
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def setup_logger():
    return logger

def load_contract_abi(abi_path):
    try:
        with open(abi_path, "r") as f:
            abi = json.load(f)
        logger.info(f"Loaded contract ABI from {abi_path}")
        return abi
    except Exception as e:
        logger.error(f"Failed to load contract ABI: {e}")
        raise

def get_contract():
    if not BTTC_CONTRACT_ADDRESS:
        logger.error("BTTC_CONTRACT_ADDRESS is not set")
        raise ValueError("BTTC_CONTRACT_ADDRESS is not set")
    abi = load_contract_abi(BTTC_CONTRACT_ABI_PATH)
    contract = w3.eth.contract(address=BTTC_CONTRACT_ADDRESS, abi=abi)
    return contract

def encrypt_data(public_key_base64, data_bytes):
    """
    Encrypt data using recipient's public key (Base64 encoded).
    """
    try:
        public_key = nacl.public.PublicKey(public_key_base64, encoder=Base64Encoder)
        sealed_box = SealedBox(public_key)
        encrypted = sealed_box.encrypt(data_bytes)
        encrypted_b64 = Base64Encoder.encode(encrypted).decode('utf-8')
        logger.info("Data encrypted successfully")
        return encrypted_b64
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise

def decrypt_data(private_key_base64, encrypted_b64):
    """
    Decrypt data using recipient's private key (Base64 encoded).
    """
    try:
        private_key = PrivateKey(private_key_base64, encoder=Base64Encoder)
        sealed_box = SealedBox(private_key)
        encrypted = Base64Encoder.decode(encrypted_b64)
        decrypted = sealed_box.decrypt(encrypted)
        logger.info("Data decrypted successfully")
        return decrypted
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise

def upload_to_btfs(file_path):
    """
    Upload a file to BTFS using the BTFS CLI.
    Returns the CID string.
    """
    try:
        result = subprocess.run([BTFS_CLI, "add", "-Q", file_path], capture_output=True, text=True, check=True)
        cid = result.stdout.strip()
        logger.info(f"File uploaded to BTFS with CID: {cid}")
        return cid
    except subprocess.CalledProcessError as e:
        logger.error(f"BTFS upload failed: {e.stderr}")
        raise

def download_from_btfs(cid, output_path):
    """
    Download a file from BTFS using the BTFS CLI.
    """
    try:
        subprocess.run([BTFS_CLI, "get", cid, "-o", output_path], check=True)
        logger.info(f"File downloaded from BTFS CID {cid} to {output_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"BTFS download failed: {e.stderr}")
        raise

def store_cid_on_bttc(wallet_address, private_key, cid):
    """
    Store the CID on BTTC smart contract mapped to the wallet address.
    """
    try:
        contract = get_contract()
        nonce = w3.eth.get_transaction_count(wallet_address)
        txn = contract.functions.storeCID(cid).build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.toWei('10', 'gwei')
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"CID stored on BTTC with tx hash: {tx_hash.hex()}")
        return tx_hash.hex()
    except Exception as e:
        logger.error(f"Failed to store CID on BTTC: {e}")
        raise

def get_cids_from_bttc(wallet_address):
    """
    Retrieve CIDs mapped to the wallet address from BTTC smart contract.
    """
    try:
        contract = get_contract()
        cids = contract.functions.getCIDs(wallet_address).call()
        logger.info(f"Retrieved {len(cids)} CIDs from BTTC for wallet {wallet_address}")
        return cids
    except Exception as e:
        logger.error(f"Failed to retrieve CIDs from BTTC: {e}")
        raise
