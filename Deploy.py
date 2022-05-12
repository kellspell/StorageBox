# Importing compiler
from brownie import chain
from rsa import PrivateKey
from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Working with the contract, you always need
# Contract Address
# Contract ABI

# This load_dotenv automatic looks for our .env files and imports in our scrpt
load_dotenv()


# This is the way that we can import a solidity file
with open("./StorageBox.sol", "r") as file:
    Storage_box_file = file.read()

    # Compile Our Solidity

    # We're going to save our compile code in a varible bellow
    # Compile our Solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"StorageBox.sol": {"content": Storage_box_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
)

# This is the way we can generate  our ABI compile file
# We do nedd off course to import json for that
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

    # To be able to deploy we need to get the bytecode and we can have it like that
bytecode = compiled_sol["contracts"]["StorageBox.sol"]["SimplaStorage"]["evm"][
    "bytecode"
]["object"]

# And also the ABI
abi = compiled_sol["contracts"]["StorageBox.sol"]["SimplaStorage"]["abi"]

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/6eb755223587473190ef017e6ae3653f"))
chain_id = 4
# Now we're going to need one wallet address and also a private key , that we can get it from ganache
my_address = "0xd1A1a01272d523E43cA1D3AB2376476aAcE5e28B"
# Remember to add 0x infront of our private key
PrivateKey = os.getenv("PRIVATE_KEY")

# Now we need to create a contract in Python
StorageBox = w3.eth.contract(abi=abi, bytecode=bytecode)

# 1 Build  the contract deploy transaction
# 2 Sign the transaction
# 3 Send the transaction

# Get the latest transaction nonce
nonce = w3.eth.getTransactionCount(my_address)

# Lets buils the transaction
transaction = StorageBox.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# This is how we signed a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PrivateKey)
print("Deploying  Contract! ")
# send this sined transaction
# Send it !

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with the contract , you always need
# Contract Address
storage_box = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Contract ABI
# when we make a transaction on the blackchain has two different ways to interact with them
# by using -> Call or Transact
# Call -> Simulating making the call and getting a return value ,dont make a state change on the blockchain
# Trasact -> Actually make a state change
print(f"Initial Stored Value {storage_box.functions.retrieve().call()}")
store_transaction = storage_box.functions.Store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=PrivateKey
)
# sending transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(storage_box.functions.retrieve().call())
