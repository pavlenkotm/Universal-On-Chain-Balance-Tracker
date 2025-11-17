"""Solana blockchain client"""

from solana.rpc.api import Client
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address
from typing import List, Optional
import logging
from ..config import SOLANA_CONFIG
from ..models import NetworkBalance, TokenBalance
from ..tokens import SOLANA_POPULAR_TOKENS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SolanaClient:
    """Client for interacting with Solana blockchain"""

    def __init__(self):
        """Initialize Solana client"""
        self.config = SOLANA_CONFIG
        self.client = Client(self.config["rpc_url"])

        # Test connection
        try:
            self.client.is_connected()
            logger.info(f"Connected to {self.config['name']}")
        except Exception as e:
            logger.warning(f"Could not connect to Solana: {e}")

    def get_native_balance(self, address: str) -> tuple[str, str]:
        """
        Get native SOL balance

        Args:
            address: Wallet address

        Returns:
            Tuple of (raw_balance_lamports, formatted_balance_sol)
        """
        try:
            pubkey = Pubkey.from_string(address)
            response = self.client.get_balance(pubkey)

            if response.value is not None:
                lamports = response.value
                sol = lamports / (10 ** self.config["decimals"])
                return str(lamports), f"{sol:.6f}".rstrip('0').rstrip('.')
            else:
                return "0", "0"

        except Exception as e:
            logger.error(f"Error getting SOL balance: {e}")
            return "0", "0"

    def get_token_balance(self, address: str, mint_address: str, decimals: int = 6) -> tuple[str, str]:
        """
        Get SPL token balance

        Args:
            address: Wallet address
            mint_address: Token mint address
            decimals: Token decimals

        Returns:
            Tuple of (raw_balance, formatted_balance)
        """
        try:
            owner_pubkey = Pubkey.from_string(address)
            mint_pubkey = Pubkey.from_string(mint_address)

            # Get associated token account
            token_account = get_associated_token_address(owner_pubkey, mint_pubkey)

            # Get token account balance
            response = self.client.get_token_account_balance(token_account)

            if response.value is not None:
                raw_balance = response.value.amount
                formatted_balance = float(raw_balance) / (10 ** decimals)
                return raw_balance, f"{formatted_balance:.6f}".rstrip('0').rstrip('.')
            else:
                return "0", "0"

        except Exception as e:
            # Token account might not exist if balance is 0
            logger.debug(f"Error getting token balance for {mint_address}: {e}")
            return "0", "0"

    def get_all_balances(self, address: str) -> NetworkBalance:
        """
        Get all balances (SOL + popular SPL tokens) for an address

        Args:
            address: Wallet address

        Returns:
            NetworkBalance object with all balances
        """
        try:
            # Get native SOL balance
            native_raw, native_formatted = self.get_native_balance(address)

            # Get SPL token balances
            token_balances = []

            for token_info in SOLANA_POPULAR_TOKENS:
                raw_balance, formatted_balance = self.get_token_balance(
                    address,
                    token_info["mint"],
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
                            contract_address=token_info["mint"]
                        )
                    )

            return NetworkBalance(
                network=self.config["name"],
                chain_id=None,  # Solana doesn't use chain_id
                native_token=self.config["native_token"],
                native_balance=native_raw,
                native_balance_formatted=native_formatted,
                tokens=token_balances,
                explorer_url=f"{self.config['explorer']}/account/{address}"
            )

        except Exception as e:
            logger.error(f"Error getting Solana balances: {e}")
            return NetworkBalance(
                network=self.config["name"],
                chain_id=None,
                native_token=self.config["native_token"],
                native_balance="0",
                native_balance_formatted="0",
                tokens=[],
                explorer_url=f"{self.config['explorer']}/account/{address}"
            )


def get_solana_balances(address: str) -> NetworkBalance:
    """
    Get Solana balances

    Args:
        address: Wallet address

    Returns:
        NetworkBalance object
    """
    try:
        client = SolanaClient()
        return client.get_all_balances(address)
    except Exception as e:
        logger.error(f"Error getting Solana balances: {e}")
        return NetworkBalance(
            network=SOLANA_CONFIG["name"],
            chain_id=None,
            native_token=SOLANA_CONFIG["native_token"],
            native_balance="0",
            native_balance_formatted="0",
            tokens=[],
            explorer_url=""
        )
