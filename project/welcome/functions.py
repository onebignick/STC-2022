# To utilise solidity functions
import json
from web3 import Web3
from pathlib import Path
from solcx import compile_standard, install_solc
from web3.middleware import geth_poa_middleware

p = Path(__file__).with_name("db.sol")

with p.open("r") as file:
    db_file = file.read()

print("Installing... test")
install_solc("0.8.7")
print("py-solcx installed!")

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

# with open("./project/welcome/compiled_code.json", "w") as file:
# json.dump(compiled_sol, file)

# Bytecode
bytecode = compiled_sol["contracts"]["db.sol"]["Users"]["evm"]["bytecode"]["object"]

# Abi
abi = json.loads(compiled_sol["contracts"]["db.sol"]["Users"]["metadata"])["output"][
    "abi"
]

# For connecting to Sepolia
# w3 = Web3(Web3.HTTPProvider("https://rpc.sepolia.dev"))
# chain_id = 11155111

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

if chain_id == 11155111:  # Sepolia chain ID is 11155111
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.clientVersion)

my_address = "0x1667a684E0bD33EdeCf74EE86B52835312bd7eEA"
private_key = "c9544cafe50f0cebcb512535e6a902fcae5ecddf7c5fd832d39ef2e645a6be56"

# jons add and key
# 0xE5ce067301e150F27F50Eb58ae078A80ab987183
# 36230e823372730c5225d10470fef124aaa6a1a2f4286f78b5eba097c8af0653

# Get contract address of deployed contract
p = Path(__file__).with_name("contractaddress.txt")

with p.open("r") as file:
    contract_address = file.read()

db = w3.eth.contract(address=contract_address, abi=abi)

# Function createNewUser creates new user in database
def createNewUser(username, password):
    print(f"Attempting to create user: {username} with password: {password}")
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = db.functions.addUser(username, password).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Signing the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Sending Transaction!")
    # Sending txn
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! User: {username} created with password: {password}")


# Function updateUser updates the password of existing user
def updateUser(username, old_password, new_password):
    print(
        f"Attempting to update user: {username} from password: {old_password} to {new_password}"
    )
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = db.functions.updateUser(
        username, old_password, new_password
    ).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Signing the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Sending Transaction!")
    # Sending txn
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! User: {username} updated with password: {new_password}")


# Function findPassword retrives password of existing user
def findPassword(username):
    return db.functions.getUser(username).call()[1]


# Function deleteUser deletes an existing user
def deleteUser(username):
    print(f"Attempting to delete user: {username}...")
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = db.functions.deleteUser(username).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    # Signing the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Sending Transaction!")
    # Sending txn
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! User: {username} deleted")


def login(username, password):
    pass


def logout(username, password):
    pass
