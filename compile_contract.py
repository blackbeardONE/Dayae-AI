import json
from solcx import compile_standard, install_solc

def compile_contract():
    # Install Solidity compiler version 0.8.0
    install_solc('0.8.0')

    with open('bttc_cid_mapping.sol', 'r') as file:
        source_code = file.read()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "bttc_cid_mapping.sol": {
                "content": source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version='0.8.0')

    # Save ABI to JSON file
    abi = compiled_sol['contracts']['bttc_cid_mapping.sol']['BTTC_CID_Mapping']['abi']
    with open('bttc_cid_mapping_abi.json', 'w') as abi_file:
        json.dump(abi, abi_file, indent=4)
    print("ABI saved to bttc_cid_mapping_abi.json")

if __name__ == "__main__":
    compile_contract()
