"""Address validators for EVM and Solana"""

from web3 import Web3
import base58
from typing import Tuple


def validate_evm_address(address: str) -> Tuple[bool, str]:
    """
    Validate EVM (Ethereum-compatible) address

    Args:
        address: Address string to validate

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        if not address:
            return False, "Address cannot be empty"

        if not address.startswith("0x"):
            return False, "EVM address must start with '0x'"

        if len(address) != 42:
            return False, f"EVM address must be 42 characters long, got {len(address)}"

        if not Web3.is_address(address):
            return False, "Invalid EVM address format"

        # Convert to checksum address
        checksum_address = Web3.to_checksum_address(address)
        return True, checksum_address

    except Exception as e:
        return False, f"Address validation error: {str(e)}"


def validate_solana_address(address: str) -> Tuple[bool, str]:
    """
    Validate Solana address

    Args:
        address: Address string to validate

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        if not address:
            return False, "Address cannot be empty"

        # Solana addresses are base58 encoded and typically 32-44 characters
        if len(address) < 32 or len(address) > 44:
            return False, f"Solana address length should be between 32-44 characters, got {len(address)}"

        # Try to decode base58
        try:
            decoded = base58.b58decode(address)
            if len(decoded) != 32:
                return False, "Invalid Solana address: decoded length must be 32 bytes"
        except Exception:
            return False, "Invalid Solana address: not valid base58"

        return True, address

    except Exception as e:
        return False, f"Address validation error: {str(e)}"


def detect_address_type(address: str) -> str:
    """
    Detect if address is EVM or Solana

    Args:
        address: Address string

    Returns:
        'evm', 'solana', or 'unknown'
    """
    if address.startswith("0x") and len(address) == 42:
        is_valid, _ = validate_evm_address(address)
        return "evm" if is_valid else "unknown"

    if len(address) >= 32 and len(address) <= 44:
        is_valid, _ = validate_solana_address(address)
        return "solana" if is_valid else "unknown"

    return "unknown"
