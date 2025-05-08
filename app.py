import os
import tempfile
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
from backend_integration import (
    setup_logger,
    encrypt_data,
    decrypt_data,
    upload_to_btfs,
    download_from_btfs,
    store_cid_on_bttc,
    get_cids_from_bttc,
)
from langchain_together import Together
from langchain.schema import HumanMessage, SystemMessage

app = FastAPI()
logger = setup_logger()

# Initialize Together AI LLM
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "56c8eeff9971269d7a7e625ff88e8a83a34a556003a5c87c289ebe9a3d8a3d2c")
llm = Together(model="deepseek-ai/DeepSeek-R1", temperature=0, together_api_key=TOGETHER_API_KEY)

class StoreDataRequest(BaseModel):
    user_wallet: str
    user_private_key: str
    user_public_key_base64: str
    data: str  # Data to store (plaintext)

class RetrieveDataRequest(BaseModel):
    user_wallet: str
    user_private_key: str

@app.post("/store_data")
async def store_data(request: StoreDataRequest):
    try:
        # Encrypt data using user's public key
        encrypted_data_b64 = encrypt_data(request.user_public_key_base64, request.data.encode('utf-8'))

        # Save encrypted data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(encrypted_data_b64.encode('utf-8'))
            tmp_file_path = tmp_file.name

        # Upload encrypted file to BTFS
        cid = upload_to_btfs(tmp_file_path)

        # Store CID on BTTC smart contract
        tx_hash = store_cid_on_bttc(request.user_wallet, request.user_private_key, cid)

        logger.info(f"Data stored successfully for wallet {request.user_wallet} with CID {cid}")

        return {"message": "Data stored successfully", "cid": cid, "tx_hash": tx_hash}
    except Exception as e:
        logger.error(f"Error in store_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrieve_data")
async def retrieve_data(request: RetrieveDataRequest):
    try:
        # Get CIDs from BTTC smart contract
        cids = get_cids_from_bttc(request.user_wallet)
        if not cids:
            return {"message": "No data found for this wallet", "data": []}

        decrypted_data_list = []

        for cid in cids:
            # Download encrypted data from BTFS
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file_path = tmp_file.name
            download_from_btfs(cid, tmp_file_path)

            # Read encrypted data
            with open(tmp_file_path, "r") as f:
                encrypted_data_b64 = f.read()

            # Decrypt data using user's private key
            decrypted_bytes = decrypt_data(request.user_private_key, encrypted_data_b64)
            decrypted_data = decrypted_bytes.decode('utf-8')
            decrypted_data_list.append({"cid": cid, "data": decrypted_data})

        logger.info(f"Data retrieved successfully for wallet {request.user_wallet}")

        return {"message": "Data retrieved successfully", "data": decrypted_data_list}
    except Exception as e:
        logger.error(f"Error in retrieve_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_prompt")
async def process_prompt(prompt: str = Form(...)):
    try:
        # Use LangChain Together AI LLM to process prompt
        system_message = SystemMessage(content="You are a helpful AI assistant for decentralized storage.")
        human_message = HumanMessage(content=prompt)
        response = llm.invoke([system_message, human_message])
        ai_response = response.content if hasattr(response, "content") else response

        logger.info(f"Processed prompt: {prompt}")

        return {"response": ai_response}
    except Exception as e:
        logger.error(f"Error in process_prompt: {e}")
        raise HTTPException(status_code=500, detail=str(e))
