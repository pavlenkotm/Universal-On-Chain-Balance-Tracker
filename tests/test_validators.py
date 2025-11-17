"""Tests for address validators"""

import pytest
from app.validators import (
    validate_evm_address,
    validate_solana_address,
    detect_address_type
)


class TestEVMAddressValidator:
    """Test EVM address validation"""

    def test_valid_evm_address(self):
        """Test validation of valid EVM address"""
        is_valid, result = validate_evm_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
        assert is_valid is True
        assert result.startswith("0x")
        assert len(result) == 42

    def test_invalid_evm_address_no_prefix(self):
        """Test validation rejects address without 0x prefix"""
        is_valid, message = validate_evm_address("742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
        assert is_valid is False
        assert "must start with '0x'" in message

    def test_invalid_evm_address_wrong_length(self):
        """Test validation rejects address with wrong length"""
        is_valid, message = validate_evm_address("0x742d35Cc")
        assert is_valid is False
        assert "must be 42 characters long" in message

    def test_empty_evm_address(self):
        """Test validation rejects empty address"""
        is_valid, message = validate_evm_address("")
        assert is_valid is False
        assert "cannot be empty" in message


class TestSolanaAddressValidator:
    """Test Solana address validation"""

    def test_valid_solana_address(self):
        """Test validation of valid Solana address"""
        is_valid, result = validate_solana_address("9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM")
        assert is_valid is True
        assert len(result) >= 32

    def test_invalid_solana_address_wrong_length(self):
        """Test validation rejects address with wrong length"""
        is_valid, message = validate_solana_address("short")
        assert is_valid is False
        assert "length should be between 32-44" in message

    def test_empty_solana_address(self):
        """Test validation rejects empty address"""
        is_valid, message = validate_solana_address("")
        assert is_valid is False
        assert "cannot be empty" in message


class TestAddressTypeDetection:
    """Test address type detection"""

    def test_detect_evm_address(self):
        """Test EVM address detection"""
        address_type = detect_address_type("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
        assert address_type == "evm"

    def test_detect_solana_address(self):
        """Test Solana address detection"""
        address_type = detect_address_type("9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM")
        assert address_type == "solana"

    def test_detect_unknown_address(self):
        """Test unknown address detection"""
        address_type = detect_address_type("invalid_address")
        assert address_type == "unknown"
