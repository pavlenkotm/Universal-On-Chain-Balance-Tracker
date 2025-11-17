"""DeFi Positions Tracker for protocols like Aave, Compound, Uniswap"""

from web3 import Web3
from typing import List, Dict, Optional
import logging
from ..config import EVM_NETWORKS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Aave V3 Pool ABI (simplified)
AAVE_POOL_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {"name": "totalCollateralBase", "type": "uint256"},
            {"name": "totalDebtBase", "type": "uint256"},
            {"name": "availableBorrowsBase", "type": "uint256"},
            {"name": "currentLiquidationThreshold", "type": "uint256"},
            {"name": "ltv", "type": "uint256"},
            {"name": "healthFactor", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Protocol addresses
DEFI_PROTOCOLS = {
    "ethereum": {
        "aave_v3_pool": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "compound_v3_usdc": "0xc3d688B66703497DAA19211EEdff47f25384cdc3",
        "uniswap_v3_positions": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
    },
    "polygon": {
        "aave_v3_pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
    },
    "arbitrum": {
        "aave_v3_pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
    },
    "optimism": {
        "aave_v3_pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
    },
    "base": {
        "aave_v3_pool": "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5",
    },
    "avalanche": {
        "aave_v3_pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
    }
}


class DeFiTracker:
    """Track DeFi positions across protocols"""

    def __init__(self, network_key: str):
        """
        Initialize DeFi tracker for specific network

        Args:
            network_key: Network identifier
        """
        if network_key not in EVM_NETWORKS:
            raise ValueError(f"Unsupported network: {network_key}")

        self.network_key = network_key
        self.config = EVM_NETWORKS[network_key]
        self.w3 = Web3(Web3.HTTPProvider(self.config["rpc_url"]))
        self.protocols = DEFI_PROTOCOLS.get(network_key, {})

    def get_aave_position(self, address: str) -> Optional[Dict]:
        """
        Get Aave lending/borrowing position

        Args:
            address: User address

        Returns:
            Dict with Aave position data or None
        """
        if "aave_v3_pool" not in self.protocols:
            return None

        try:
            checksum_address = Web3.to_checksum_address(address)
            pool_address = Web3.to_checksum_address(self.protocols["aave_v3_pool"])

            contract = self.w3.eth.contract(address=pool_address, abi=AAVE_POOL_ABI)

            account_data = contract.functions.getUserAccountData(checksum_address).call()

            total_collateral = account_data[0]
            total_debt = account_data[1]
            available_borrows = account_data[2]
            health_factor = account_data[5]

            # Only return if user has position
            if total_collateral == 0 and total_debt == 0:
                return None

            # Convert from base units (8 decimals for USD value in Aave)
            return {
                "protocol": "Aave V3",
                "network": self.config["name"],
                "total_collateral_usd": str(total_collateral / 1e8),
                "total_debt_usd": str(total_debt / 1e8),
                "available_borrows_usd": str(available_borrows / 1e8),
                "health_factor": str(health_factor / 1e18) if health_factor > 0 else "N/A",
                "net_worth_usd": str((total_collateral - total_debt) / 1e8)
            }

        except Exception as e:
            logger.debug(f"Error getting Aave position on {self.network_key}: {e}")
            return None

    def get_all_positions(self, address: str) -> List[Dict]:
        """
        Get all DeFi positions

        Args:
            address: User address

        Returns:
            List of DeFi positions
        """
        positions = []

        # Check Aave
        aave_position = self.get_aave_position(address)
        if aave_position:
            positions.append(aave_position)

        # Add more protocols here (Compound, Uniswap, etc.)
        # compound_position = self.get_compound_position(address)
        # uniswap_positions = self.get_uniswap_positions(address)

        return positions


def get_defi_positions(address: str, networks: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
    """
    Get DeFi positions across multiple networks

    Args:
        address: User address
        networks: List of network keys (None = all networks)

    Returns:
        Dict mapping network to DeFi positions
    """
    if networks is None:
        networks = list(EVM_NETWORKS.keys())

    all_positions = {}

    for network_key in networks:
        try:
            tracker = DeFiTracker(network_key)
            positions = tracker.get_all_positions(address)
            if positions:
                all_positions[network_key] = positions
        except Exception as e:
            logger.error(f"Error getting DeFi positions for {network_key}: {e}")
            continue

    return all_positions
