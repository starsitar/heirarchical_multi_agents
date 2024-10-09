from web3 import Web3
from eth_account import Account
import os
import requests
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

# Load environment variables
load_dotenv()

# Ensure Web3 is initialized
infura_url = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))

# ERC20 ABI (You will need to provide this for token interaction)
erc20_abi = '[...]'  # Placeholder for the actual ERC20 ABI

### Wallet & Balance Queries ###
def get_eth_balance(wallet_address):
    try:
        balance = web3.eth.get_balance(wallet_address)  # Directly use the address
        return f"The ETH balance for {wallet_address} is {balance} ETH"
    except Exception as e:
        return f"Error fetching balance: {str(e)}"

def get_token_balance(wallet_address, token_address):
    # Define the ERC20 ABI (minimum needed for balanceOf)
    erc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        }
    ]
    try:
        # Convert both the wallet and token addresses to checksum addresses
        wallet_address = Web3.to_checksum_address(wallet_address)
        token_address = Web3.to_checksum_address(token_address)
        
        # Initialize contract with the token address and ERC20 ABI
        contract = web3.eth.contract(address=token_address, abi=erc20_abi)
        
        # Call the balanceOf function to get the token balance
        balance = contract.functions.balanceOf(wallet_address).call()
        
        # Assuming token uses 18 decimals by default, adjust it accordingly.
        balance_in_tokens = balance / (10 ** 18)  # Adjust based on actual token decimals
        return f"The balance for {wallet_address} is {balance_in_tokens} tokens"
    except Exception as e:
        return f"Error fetching token balance: {str(e)}"
    
### Transaction Queries ###
def get_transaction_status(tx_hash):
    try:
        receipt = web3.eth.getTransactionReceipt(tx_hash)
        if receipt is None:
            return "Transaction is pending"
        elif receipt['status'] == 1:
            return "Transaction successful"
        else:
            return "Transaction failed"
    except Exception as e:
        return f"Error fetching transaction status: {str(e)}"

def get_recent_transactions(wallet_address):
    try:
        block = web3.eth.get_block('latest')
        return block['transactions'][:10]  # Fetch recent transactions (you can extend this)
    except Exception as e:
        return f"Error fetching recent transactions: {str(e)}"

def estimate_gas_fee():
    try:
        return web3.eth.gas_price
    except Exception as e:
        return f"Error fetching gas fees: {str(e)}"

### Swap & DeFi Queries ###
def perform_token_swap(wallet_address, token_from, token_to, amount):
    try:
        # Placeholder for actual token swap logic using a DEX like Uniswap
        tx_hash = "0x123456789abcdef"  # Dummy transaction hash
        return f"Swap transaction submitted: {tx_hash}"
    except Exception as e:
        return f"Error performing swap: {str(e)}"

def get_best_swap_rate(token_from, token_to):
    try:
        # Call a price aggregator API like 1inch, matcha, etc.
        return {"rate": "Best rate fetched from DEX aggregators"}
    except Exception as e:
        return f"Error fetching swap rate: {str(e)}"

### NFT Queries ###
def get_nft_collection(wallet_address):
    try:
        # Placeholder for fetching NFT collection
        return {"nfts": "List of NFTs owned by the wallet"}
    except Exception as e:
        return f"Error fetching NFT collection: {str(e)}"

def get_nft_value(nft_address):
    try:
        # Placeholder for querying NFT price
        return {"nft_value": "Estimated value of the NFT"}
    except Exception as e:
        return f"Error fetching NFT value: {str(e)}"

### Market Data & Analytics ###
def get_token_price(token_address):
    try:
        # Query from CoinGecko, CoinMarketCap, or other APIs
        return {"price": "Current token price from market"}
    except Exception as e:
        return f"Error fetching token price: {str(e)}"

def get_historical_prices(token_address):
    try:
        # Placeholder for fetching historical price data
        return {"historical_prices": "Historical prices data"}
    except Exception as e:
        return f"Error fetching historical prices: {str(e)}"

### Staking & Yield Farming ###
def get_staking_opportunities(token_address):
    try:
        # Query DeFi platforms for staking pools
        return {"staking_options": "List of staking opportunities"}
    except Exception as e:
        return f"Error fetching staking opportunities: {str(e)}"

def calculate_staking_yield(token_address, amount):
    try:
        # Fetch staking rates and calculate yield
        return {"apy": "Calculated APY based on staking"}
    except Exception as e:
        return f"Error calculating staking yield: {str(e)}"

### Security & Wallet Management ###
def create_wallet():
    try:
        account = Account.create()
        return {"address": account.address, "private_key": account.privateKey.hex()}
    except Exception as e:
        return f"Error creating wallet: {str(e)}"

def get_private_key(wallet_address):
    # Not recommended for production use, as exposing private keys is dangerous.
    return "Private key management should be done securely."

### Contract Queries ###
def call_smart_contract_function(contract_address, function_name, *args):
    try:
        contract = web3.eth.contract(address=contract_address, abi=erc20_abi)  # Adjust ABI as needed
        func = getattr(contract.functions, function_name)
        tx_hash = func(*args).transact({'from': web3.eth.accounts[0]})
        return f"Function {function_name} called, transaction: {tx_hash}"
    except Exception as e:
        return f"Error calling smart contract function: {str(e)}"

def get_contract_data(contract_address, function_name):
    try:
        contract = web3.eth.contract(address=contract_address, abi=erc20_abi)  # Adjust ABI as needed
        data = getattr(contract.functions, function_name)().call()
        return data
    except Exception as e:
        return f"Error fetching contract data: {str(e)}"

### Cross-Chain Queries ###
def bridge_tokens(wallet_address, token_address, amount, target_chain):
    try:
        # Interact with cross-chain bridges
        return {"status": "Bridge transaction submitted"}
    except Exception as e:
        return f"Error bridging tokens: {str(e)}"

### Governance & Voting ###
def vote_on_proposal(proposal_id, wallet_address, vote_choice):
    try:
        # Logic to vote on governance proposals
        return {"status": f"Vote submitted for proposal {proposal_id}"}
    except Exception as e:
        return f"Error submitting vote: {str(e)}"

def get_governance_tokens(wallet_address):
    try:
        # Query the balance of governance tokens in the wallet
        return {"tokens": "List of governance tokens held by wallet"}
    except Exception as e:
        return f"Error fetching governance tokens: {str(e)}"
    
import requests

def lookup_token_address(token_name):
    """
    Lookup the Ethereum contract address for a given token name using CoinGecko API.
    
    Args:
        token_name (str): The name of the token (e.g., "USDC", "DAI").

    Returns:
        str: The contract address of the token or an error message.
    """
    try:
        # CoinGecko API endpoint for token information
        url = f"https://api.coingecko.com/api/v3/coins/{token_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            platforms = data.get("platforms", {})
            token_address = platforms.get("ethereum", "Token address not found on Ethereum network.")
            return token_address
        else:
            return f"Error: Unable to retrieve token data (status code {response.status_code})."
    except Exception as e:
        return f"Error: {str(e)}"
    

def get_tokens_from_etherscan(wallet_address):
    """
    Get the list of ERC20 tokens held by a given Ethereum wallet address using the Etherscan API.
    
    Args:
        wallet_address (str): The Ethereum wallet address.

    Returns:
        str: A formatted list of tokens and their balances.
    """
    try:
        # Load Etherscan API key from environment
        etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
        if not etherscan_api_key:
            return "Error: Etherscan API key is not found in environment variables."

        # Etherscan API endpoint for getting token balances (ERC20)
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={etherscan_api_key}"

        # Make the request to Etherscan API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json().get("result", [])
            if not data:
                return f"No tokens found in wallet {wallet_address}"

            # Prepare the list of tokens and balances
            token_balances = {}
            for token in data:
                token_name = token['tokenName']
                token_symbol = token['tokenSymbol']
                token_contract = token['contractAddress']
                token_value = int(token['value']) / (10 ** int(token['tokenDecimal']))

                if token_contract not in token_balances:
                    token_balances[token_contract] = {"name": token_name, "symbol": token_symbol, "balance": 0}

                token_balances[token_contract]["balance"] += token_value

            # Format the output
            token_list = [f"{info['symbol']}: {info['balance']:.4f}" for info in token_balances.values()]
            return f"Tokens in {wallet_address}:\n" + "\n".join(token_list)
        else:
            return f"Error: Unable to retrieve token data (status code {response.status_code})."
    
    except Exception as e:
        return f"Error fetching token balances: {str(e)}"


def get_nfts_from_etherscan(wallet_address):
    """
    Get the list of NFTs held by a given Ethereum wallet address using the Etherscan API.
    
    Args:
        wallet_address (str): The Ethereum wallet address.

    Returns:
        str: A formatted list of NFTs.
    """
    try:
        # Load Etherscan API key from environment
        etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
        if not etherscan_api_key:
            return "Error: Etherscan API key is not found in environment variables."

        # Etherscan API endpoint for getting ERC721 token transfers
        url = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={etherscan_api_key}"

        # Make the request to Etherscan API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            nfts = response.json().get("result", [])
            if not nfts:
                return f"No NFTs found in wallet {wallet_address}"

            # Prepare the list of NFTs
            nft_list = []
            for nft in nfts:
                contract = nft['contractAddress']
                token_id = nft['tokenID']
                name = nft.get('tokenName', 'Unknown NFT')
                symbol = nft.get('tokenSymbol', 'NFT')
                nft_list.append(f"{name} (Symbol: {symbol}, Token ID: {token_id}, Contract: {contract})")

            return f"NFTs in {wallet_address}:\n" + "\n".join(nft_list)
        else:
            return f"Error: Unable to retrieve NFT data (status code {response.status_code})."
    
    except Exception as e:
        return f"Error fetching NFTs: {str(e)}"
    
# Load and preprocess plans from a text file
def load_common_plans(filepath="common_plans.txt"):
    with open(filepath, "r") as file:
        plans = [line.strip() for line in file]
    return plans

# Initialize OpenAI Embeddings
embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Load the plans and wrap them into Document objects
plans = load_common_plans()
documents = [Document(page_content=plan) for plan in plans]

# Create a FAISS index for similarity search
faiss_index = FAISS.from_documents(documents, embedding_model)


def find_similar_plan(user_input: str):
    """
    Finds the most similar plan from a list of common plans based on the user's query.
    """
    try:
        # Search for the most similar plan using FAISS
        search_results = faiss_index.similarity_search(user_input, k=1)
        best_match_plan = search_results[0].page_content
        
        return f"Most similar plan: {best_match_plan}"
    
    except Exception as e:
        return f"Error finding similar plan: {str(e)}"