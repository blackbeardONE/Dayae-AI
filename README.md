This project needs a lot of time and hardware requirements. Help me accomplish my goal of serving humanity new technology for better life. Buy me a coffee! >>
https://ko-fi.com/joedeldalioan

or send me some love via paypal or crypto >>

- **Paypal:** paypal.me/Dalioan
- **Bitcoin (Unisat):** bc1qu8pknsrwvssspq4c6a5j4p3x835phq8n3ajcgw
- **Solana:** FNEdD3PWMLwbNKxtaHy3W2NVfRJ7wqDNx4M9je8Xc6Mw
- **Tron:** TGVrpryTJAmWEPWTKYB3tGRv5gWhE2g9Lo
- **Metamask:** 0x9F32B8346bD728DF3AB7775971705D02fb86dD9c

# Decentralized AI-Assisted Storage & Retrieval System

## Overview
This project is a secure, decentralized system where users interact with AI to store and retrieve data on BTFS (BitTorrent File System) with access control via BTTC (BitTorrent Chain). It integrates AI processing, encryption, decentralized storage, and blockchain-based access control to provide a privacy-preserving data management solution.

## Architecture
User → Frontend → AI (LangChain/LLM) → BTFS (Encrypted Data) ↔ BTTC (CID Mapping)

- Users upload data via prompts.
- AI encrypts data and stores it on BTFS, returning a Content Identifier (CID).
- The CID is recorded on the BTTC blockchain smart contract mapped to the user's wallet.
- For retrieval, AI queries BTTC for CIDs, fetches encrypted data from BTFS, decrypts it, and responds.

## Tech Stack
- **AI & Backend:** Python, LangChain, Together AI API, FastAPI/Flask
- **Storage:** BTFS CLI/SDK, Web3.storage
- **Blockchain:** Solidity (BTTC smart contracts), Hardhat, ethers.js/web3.py
- **Encryption:** libsodium (NaCl), MetaMask (key management)
- **Frontend:** React + Vite, ethers.js, Tailwind CSS
- **Data Indexing:** Pinecone/FAISS (vector DB for prompt-CID mapping)

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.8+
- BTFS CLI installed and running
- MetaMask wallet for blockchain interactions

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install Node.js dependencies (for frontend and smart contract dapps):
   ```bash
   cd references/BTTC\ sample\ implementation/dapp-ui
   npm install
   ```

3. Install Python dependencies:
   ```bash
   cd references/Together\ AI\ sample\ implementation
   pip install -r requirements.txt
   ```

4. Set up BTFS node and BTTC smart contracts as per documentation in `references/BTTC sample implementation/README.md`.

## Usage
- Run the AI backend to process prompts and interact with BTFS and BTTC.
- Use the frontend dapp to login with MetaMask, upload data, and retrieve stored data securely.

## Contributing
Contributions are welcome! Please open issues or pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Developer 👨‍💻

Developed by [Blackbeard](https://blackbeard.one) | [Ten Titanics](https://tentitanics.com) | [GitHub](https://github.com/blackbeardONE)

© 2023-2025 Blackbeard. All rights reserved.# QSDM