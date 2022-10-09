import json
from numpy import sign

from web3 import Web3

from solcx import compile_standard, install_solc
import os
from web3.middleware import geth_poa_middleware

with open("./db.sol", "r") as file:
    db_file = file.read()

print("Installing...")
install_solc("0.8.7")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"db.sol": {"content": db_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.7",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Bytecode
bytecode = compiled_sol["contracts"]["db.sol"]["passwordStorage"]["evm"]["bytecode"][
    "object"
]

# Abi
abi = json.loads(compiled_sol["contracts"]["db.sol"]["passwordStorage"]["metadata"])[
    "output"
]["abi"]

# For connecting to Sepolia

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

if chain_id == 11155111:  # Sepolia chain ID is 11155111
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.clientVersion)

my_address = "0x1667a684E0bD33EdeCf74EE86B52835312bd7eEA"
private_key = "c9544cafe50f0cebcb512535e6a902fcae5ecddf7c5fd832d39ef2e645a6be56"

# Creating the contract in python
db = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transation that deploys the contract
transaction = db.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# Signing the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Sending txn
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
