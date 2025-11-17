"""NFT Balance Tracker for ERC721 and ERC1155 tokens"""

from web3 import Web3
from typing import List, Dict, Optional
import logging
from ..config import EVM_NETWORKS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ERC721 ABI (minimal for balance checking)
ERC721_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}, {"name": "index", "type": "uint256"}],
        "name": "tokenOfOwnerByIndex",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]

# Popular NFT collections per network
POPULAR_NFTS = {
    "ethereum": [
        {"name": "Bored Ape Yacht Club", "address": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"},
        {"name": "Mutant Ape Yacht Club", "address": "0x60E4d786628Fea6478F785A6d7e704777c86a7c6"},
        {"name": "Azuki", "address": "0xED5AF388653567Af2F388E6224dC7C4b3241C544"},
        {"name": "CloneX", "address": "0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B"},
        {"name": "Doodles", "address": "0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e"},
    ],
    "polygon": [
        {"name": "Sandbox Land", "address": "0x9d305a42A3975Ee4c1C57555BeD5919889DCE63F"},
    ],
    "arbitrum": [],
    "optimism": [],
    "base": [],
}


class NFTTracker:
    """Track NFT balances across EVM networks"""

    def __init__(self, network_key: str):
        """
        Initialize NFT tracker for specific network

        Args:
            network_key: Network identifier
        """
        if network_key not in EVM_NETWORKS:
            raise ValueError(f"Unsupported network: {network_key}")

        self.network_key = network_key
        self.config = EVM_NETWORKS[network_key]
        self.w3 = Web3(Web3.HTTPProvider(self.config["rpc_url"]))

    def get_nft_balance(self, address: str, nft_contract: str) -> Dict:
        """
        Get NFT balance for a specific contract

        Args:
            address: Owner address
            nft_contract: NFT contract address

        Returns:
            Dict with NFT info and balance
        """
        try:
            checksum_address = Web3.to_checksum_address(address)
            nft_checksum = Web3.to_checksum_address(nft_contract)

            contract = self.w3.eth.contract(address=nft_checksum, abi=ERC721_ABI)

            # Get balance
            balance = contract.functions.balanceOf(checksum_address).call()

            if balance == 0:
                return None

            # Get collection info
            try:
                name = contract.functions.name().call()
                symbol = contract.functions.symbol().call()
            except Exception:
                name = "Unknown"
                symbol = "NFT"

            # Try to get token IDs
            token_ids = []
            try:
                for i in range(min(balance, 10)):  # Limit to first 10 tokens
                    token_id = contract.functions.tokenOfOwnerByIndex(checksum_address, i).call()
                    token_ids.append(str(token_id))
            except Exception:
                # If tokenOfOwnerByIndex not supported, skip token IDs
                pass

            return {
                "contract_address": nft_contract,
                "name": name,
                "symbol": symbol,
                "balance": balance,
                "token_ids": token_ids[:10],  # Return max 10 token IDs
                "network": self.config["name"]
            }

        except Exception as e:
            logger.debug(f"Error getting NFT balance for {nft_contract}: {e}")
            return None

    def get_all_nfts(self, address: str) -> List[Dict]:
        """
        Get all NFT balances for popular collections

        Args:
            address: Owner address

        Returns:
            List of NFT holdings
        """
        nft_holdings = []
        popular_collections = POPULAR_NFTS.get(self.network_key, [])

        for collection in popular_collections:
            nft_info = self.get_nft_balance(address, collection["address"])
            if nft_info:
                nft_info["collection_name"] = collection["name"]
                nft_holdings.append(nft_info)

        return nft_holdings


def get_nft_balances(address: str, networks: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
    """
    Get NFT balances across multiple networks

    Args:
        address: Owner address
        networks: List of network keys (None = all networks)

    Returns:
        Dict mapping network to NFT holdings
    """
    if networks is None:
        networks = list(EVM_NETWORKS.keys())

    all_nfts = {}

    for network_key in networks:
        try:
            tracker = NFTTracker(network_key)
            nfts = tracker.get_all_nfts(address)
            if nfts:
                all_nfts[network_key] = nfts
        except Exception as e:
            logger.error(f"Error getting NFTs for {network_key}: {e}")
            continue

    return all_nfts
