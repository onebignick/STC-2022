from web3 import Web3
from web3.middleware import geth_poa_middleware
from project.welcome.deploy import get_contract_address, get_abi, get_bytecode

ca = get_contract_address()
abi = get_abi()
bytecode = get_bytecode()

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

w3.eth.contract(address=ca, abi=abi)
