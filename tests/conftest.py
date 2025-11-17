"""Pytest configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
import os

# Set test environment variables
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_db"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"


@pytest.fixture
def test_evm_address():
    """Fixture providing a test EVM address"""
    return "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"


@pytest.fixture
def test_solana_address():
    """Fixture providing a test Solana address"""
    return "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"


@pytest.fixture
def api_client():
    """Fixture providing FastAPI test client"""
    from api import app
    return TestClient(app)


@pytest.fixture
def mock_balance_data():
    """Fixture providing mock balance data"""
    return {
        "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        "networks": [
            {
                "network": "Ethereum",
                "native_balance": "1000000000000000000",
                "native_balance_formatted": "1.0",
                "tokens": []
            }
        ]
    }
