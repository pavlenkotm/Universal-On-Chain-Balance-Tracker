"""Configuration for blockchain networks and RPC endpoints"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


# EVM Networks Configuration
EVM_NETWORKS = {
    "ethereum": {
        "name": "Ethereum",
        "chain_id": 1,
        "rpc_url": os.getenv("ETHEREUM_RPC", "https://eth.llamarpc.com"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://etherscan.io"
    },
    "arbitrum": {
        "name": "Arbitrum One",
        "chain_id": 42161,
        "rpc_url": os.getenv("ARBITRUM_RPC", "https://arb1.arbitrum.io/rpc"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://arbiscan.io"
    },
    "optimism": {
        "name": "Optimism",
        "chain_id": 10,
        "rpc_url": os.getenv("OPTIMISM_RPC", "https://mainnet.optimism.io"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://optimistic.etherscan.io"
    },
    "base": {
        "name": "Base",
        "chain_id": 8453,
        "rpc_url": os.getenv("BASE_RPC", "https://mainnet.base.org"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://basescan.org"
    },
    "bnb": {
        "name": "BNB Smart Chain",
        "chain_id": 56,
        "rpc_url": os.getenv("BNB_RPC", "https://bsc-dataseed.binance.org"),
        "native_token": "BNB",
        "decimals": 18,
        "explorer": "https://bscscan.com"
    },
    "polygon": {
        "name": "Polygon",
        "chain_id": 137,
        "rpc_url": os.getenv("POLYGON_RPC", "https://polygon-rpc.com"),
        "native_token": "MATIC",
        "decimals": 18,
        "explorer": "https://polygonscan.com"
    },
    "avalanche": {
        "name": "Avalanche C-Chain",
        "chain_id": 43114,
        "rpc_url": os.getenv("AVALANCHE_RPC", "https://api.avax.network/ext/bc/C/rpc"),
        "native_token": "AVAX",
        "decimals": 18,
        "explorer": "https://snowtrace.io"
    },
    "fantom": {
        "name": "Fantom Opera",
        "chain_id": 250,
        "rpc_url": os.getenv("FANTOM_RPC", "https://rpc.ftm.tools"),
        "native_token": "FTM",
        "decimals": 18,
        "explorer": "https://ftmscan.com"
    },
    "cronos": {
        "name": "Cronos",
        "chain_id": 25,
        "rpc_url": os.getenv("CRONOS_RPC", "https://evm.cronos.org"),
        "native_token": "CRO",
        "decimals": 18,
        "explorer": "https://cronoscan.com"
    },
    "gnosis": {
        "name": "Gnosis Chain",
        "chain_id": 100,
        "rpc_url": os.getenv("GNOSIS_RPC", "https://rpc.gnosischain.com"),
        "native_token": "xDAI",
        "decimals": 18,
        "explorer": "https://gnosisscan.io"
    },
    "zksync": {
        "name": "zkSync Era",
        "chain_id": 324,
        "rpc_url": os.getenv("ZKSYNC_RPC", "https://mainnet.era.zksync.io"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://explorer.zksync.io"
    },
    "linea": {
        "name": "Linea",
        "chain_id": 59144,
        "rpc_url": os.getenv("LINEA_RPC", "https://rpc.linea.build"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://lineascan.build"
    },
    "scroll": {
        "name": "Scroll",
        "chain_id": 534352,
        "rpc_url": os.getenv("SCROLL_RPC", "https://rpc.scroll.io"),
        "native_token": "ETH",
        "decimals": 18,
        "explorer": "https://scrollscan.com"
    }
}

# Solana Configuration
SOLANA_CONFIG = {
    "name": "Solana",
    "rpc_url": os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com"),
    "native_token": "SOL",
    "decimals": 9,
    "explorer": "https://solscan.io"
}

# ERC20 ABI for balanceOf function
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
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
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]
