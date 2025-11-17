"""EVM (Ethereum Virtual Machine) blockchain client"""

from web3 import Web3
from typing import Dict, List, Optional
import logging
from ..config import EVM_NETWORKS, ERC20_ABI
from ..models import NetworkBalance, TokenBalance
from ..tokens import POPULAR_TOKENS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EVMClient:
    """Client for interacting with EVM-compatible blockchains"""

    def __init__(self, network_key: str):
        """
        Initialize EVM client for specific network

        Args:
            network_key: Network identifier (e.g., 'ethereum', 'polygon')
        """
        if network_key not in EVM_NETWORKS:
            raise ValueError(f"Unsupported network: {network_key}")

        self.network_key = network_key
        self.config = EVM_NETWORKS[network_key]
        self.w3 = Web3(Web3.HTTPProvider(self.config["rpc_url"]))

        # Test connection
        try:
            self.w3.is_connected()
            logger.info(f"Connected to {self.config['name']}")
        except Exception as e:
            logger.warning(f"Could not connect to {self.config['name']}: {e}")

    def get_native_balance(self, address: str) -> tuple[str, str]:
        """
        Get native token balance (ETH, BNB, MATIC, etc.)

        Args:
            address: Wallet address

        Returns:
            Tuple of (raw_balance, formatted_balance)
        """
        try:
            checksum_address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(checksum_address)
            balance_formatted = self.w3.from_wei(balance_wei, 'ether')
            return str(balance_wei), str(balance_formatted)
        except Exception as e:
            logger.error(f"Error getting native balance on {self.network_key}: {e}")
            return "0", "0.0"

    def get_token_balance(self, address: str, token_address: str, decimals: int = 18) -> tuple[str, str]:
        """
        Get ERC20 token balance

        Args:
            address: Wallet address
            token_address: Token contract address
            decimals: Token decimals

        Returns:
            Tuple of (raw_balance, formatted_balance)
        """
        try:
            checksum_address = Web3.to_checksum_address(address)
            token_checksum = Web3.to_checksum_address(token_address)

            contract = self.w3.eth.contract(address=token_checksum, abi=ERC20_ABI)
            balance = contract.functions.balanceOf(checksum_address).call()

            # Format balance
            balance_formatted = balance / (10 ** decimals)

            return str(balance), f"{balance_formatted:.6f}".rstrip('0').rstrip('.')
        except Exception as e:
            logger.error(f"Error getting token balance for {token_address} on {self.network_key}: {e}")
            return "0", "0"

    def get_all_balances(self, address: str) -> NetworkBalance:
        """
        Get all balances (native + popular tokens) for an address

        Args:
            address: Wallet address

        Returns:
            NetworkBalance object with all balances
        """
        try:
            # Get native balance
            native_raw, native_formatted = self.get_native_balance(address)

            # Get token balances
            token_balances = []
            popular_tokens = POPULAR_TOKENS.get(self.network_key, [])

            for token_info in popular_tokens:
                raw_balance, formatted_balance = self.get_token_balance(
                    address,
                    token_info["address"],
                    int(token_info["decimals"])
                )

                # Only include tokens with non-zero balance
                if float(formatted_balance) > 0:
                    token_balances.append(
                        TokenBalance(
                            symbol=token_info["symbol"],
                            name=token_info["name"],
                            balance=raw_balance,
                            balance_formatted=formatted_balance,
                            decimals=int(token_info["decimals"]),
                            contract_address=token_info["address"]
                        )
                    )

            return NetworkBalance(
                network=self.config["name"],
                chain_id=self.config["chain_id"],
                native_token=self.config["native_token"],
                native_balance=native_raw,
                native_balance_formatted=native_formatted,
                tokens=token_balances,
                explorer_url=f"{self.config['explorer']}/address/{address}"
            )

        except Exception as e:
            logger.error(f"Error getting balances for {self.network_key}: {e}")
            return NetworkBalance(
                network=self.config["name"],
                chain_id=self.config["chain_id"],
                native_token=self.config["native_token"],
                native_balance="0",
                native_balance_formatted="0.0",
                tokens=[],
                explorer_url=f"{self.config['explorer']}/address/{address}"
            )


def get_all_evm_balances(address: str) -> List[NetworkBalance]:
    """
    Get balances across all supported EVM networks

    Args:
        address: Wallet address

    Returns:
        List of NetworkBalance objects
    """
    balances = []

    for network_key in EVM_NETWORKS.keys():
        try:
            client = EVMClient(network_key)
            network_balance = client.get_all_balances(address)
            balances.append(network_balance)
        except Exception as e:
            logger.error(f"Error processing {network_key}: {e}")
            continue

    return balances
