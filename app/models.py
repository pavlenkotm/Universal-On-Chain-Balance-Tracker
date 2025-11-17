"""Data models for balance tracker"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class TokenBalance(BaseModel):
    """Token balance model"""
    symbol: str
    name: str
    balance: str
    balance_formatted: str
    decimals: int
    contract_address: Optional[str] = None


class NetworkBalance(BaseModel):
    """Network balance model"""
    network: str
    chain_id: Optional[int] = None
    native_token: str
    native_balance: str
    native_balance_formatted: str
    tokens: List[TokenBalance] = Field(default_factory=list)
    explorer_url: Optional[str] = None


class BalanceResponse(BaseModel):
    """Complete balance response"""
    address: str
    networks: List[NetworkBalance]
    total_networks_checked: int
    success: bool = True
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    details: Optional[str] = None
