import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# Charger les variables du fichier .env en local (ignoré automatiquement sur GitHub Actions)
load_dotenv()

# Installation de la version Solidity
print("Installation du compilateur Solidity...")
install_solc("0.8.20")

# Lecture du contrat Solidity
with open("StudentRegistry.sol", "r", encoding="utf-8") as f:
    contract_source_code = f.read()

# Compilation automatique
print("Compilation du Smart Contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"StudentRegistry.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.20",
)

contract_interface = compiled_sol["contracts"]["StudentRegistry.sol"][
    "StudentRegistry"
]
abi = contract_interface["abi"]
bytecode = contract_interface["evm"]["bytecode"]["object"]

# Connexion Sepolia via les variables d'environnement (.env ou secrets GitHub)
RPC_URL = os.getenv("WEB3_PROVIDER_URI")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# --- LIGNES DE DEBUG ---
print("--- TEST DE LECTURE DES VARIABLES ---")
print("RPC_URL =", RPC_URL)
print("-------------------------------------")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("Erreur : Impossible de se connecter au réseau Sepolia.")
    exit(1)

account = w3.eth.account.from_key(PRIVATE_KEY)
print(f"Déploiement avec le compte : {account.address}")

# Déploiement
StudentRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account.address)
construct_txn = StudentRegistry.constructor().build_transaction(
    {
        "from": account.address,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_txn = w3.eth.account.sign_transaction(
    construct_txn, private_key=PRIVATE_KEY
)
print("Envoi de la transaction sur Sepolia...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

deployed_address = tx_receipt.contractAddress
print(f"Smart Contract déployé avec succès ! Adresse : {deployed_address}")

# Sauvegarde automatique de l'adresse dans config.json pour le HTML
config = {"contractAddress": deployed_address}
with open("config.json", "w") as f:
    json.dump(config, f)
print("Fichier config.json mis à jour avec succès.")