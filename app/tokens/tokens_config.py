"""Popular tokens configuration for each network"""

from typing import Dict, List

# Popular tokens for each EVM network
POPULAR_TOKENS: Dict[str, List[Dict[str, str]]] = {
    "ethereum": [
        {
            "symbol": "USDT",
            "name": "Tether USD",
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": "6"
        },
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "decimals": "6"
        },
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "decimals": "18"
        },
        {
            "symbol": "DAI",
            "name": "Dai Stablecoin",
            "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "decimals": "18"
        },
        {
            "symbol": "WBTC",
            "name": "Wrapped BTC",
            "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            "decimals": "8"
        },
        {
            "symbol": "LINK",
            "name": "ChainLink Token",
            "address": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
            "decimals": "18"
        },
        {
            "symbol": "UNI",
            "name": "Uniswap",
            "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
            "decimals": "18"
        }
    ],
    "arbitrum": [
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "decimals": "6"
        },
        {
            "symbol": "USDT",
            "name": "Tether USD",
            "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
            "decimals": "6"
        },
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
            "decimals": "18"
        },
        {
            "symbol": "ARB",
            "name": "Arbitrum",
            "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
            "decimals": "18"
        },
        {
            "symbol": "WBTC",
            "name": "Wrapped BTC",
            "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
            "decimals": "8"
        }
    ],
    "optimism": [
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
            "decimals": "6"
        },
        {
            "symbol": "USDT",
            "name": "Tether USD",
            "address": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
            "decimals": "6"
        },
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0x4200000000000000000000000000000000000006",
            "decimals": "18"
        },
        {
            "symbol": "OP",
            "name": "Optimism",
            "address": "0x4200000000000000000000000000000000000042",
            "decimals": "18"
        },
        {
            "symbol": "WBTC",
            "name": "Wrapped BTC",
            "address": "0x68f180fcCe6836688e9084f035309E29Bf0A2095",
            "decimals": "8"
        }
    ],
    "base": [
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "decimals": "6"
        },
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0x4200000000000000000000000000000000000006",
            "decimals": "18"
        },
        {
            "symbol": "DAI",
            "name": "Dai Stablecoin",
            "address": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
            "decimals": "18"
        }
    ],
    "bnb": [
        {
            "symbol": "USDT",
            "name": "Tether USD",
            "address": "0x55d398326f99059fF775485246999027B3197955",
            "decimals": "18"
        },
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "decimals": "18"
        },
        {
            "symbol": "WBNB",
            "name": "Wrapped BNB",
            "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            "decimals": "18"
        },
        {
            "symbol": "BUSD",
            "name": "Binance USD",
            "address": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
            "decimals": "18"
        },
        {
            "symbol": "BTCB",
            "name": "Bitcoin BEP2",
            "address": "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
            "decimals": "18"
        },
        {
            "symbol": "CAKE",
            "name": "PancakeSwap Token",
            "address": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
            "decimals": "18"
        }
    ],
    "polygon": [
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
            "decimals": "6"
        },
        {
            "symbol": "USDT",
            "name": "Tether USD",
            "address": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
            "decimals": "6"
        },
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
            "decimals": "18"
        },
        {
            "symbol": "WMATIC",
            "name": "Wrapped Matic",
            "address": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
            "decimals": "18"
        },
        {
            "symbol": "WBTC",
            "name": "Wrapped BTC",
            "address": "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6",
            "decimals": "8"
        },
        {
            "symbol": "DAI",
            "name": "Dai Stablecoin",
            "address": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            "decimals": "18"
        }
    ]
}

# Popular SPL tokens for Solana
SOLANA_POPULAR_TOKENS = [
    {
        "symbol": "USDC",
        "name": "USD Coin",
        "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "decimals": "6"
    },
    {
        "symbol": "USDT",
        "name": "Tether USD",
        "mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
        "decimals": "6"
    },
    {
        "symbol": "BONK",
        "name": "Bonk",
        "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
        "decimals": "5"
    },
    {
        "symbol": "JUP",
        "name": "Jupiter",
        "mint": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "decimals": "6"
    },
    {
        "symbol": "RAY",
        "name": "Raydium",
        "mint": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
        "decimals": "6"
    }
]
