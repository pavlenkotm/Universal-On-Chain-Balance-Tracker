"""Price feeds integration with CoinGecko and CoinMarketCap"""

import os
import requests
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token ID mappings for CoinGecko
COINGECKO_IDS = {
    "ETH": "ethereum",
    "BTC": "bitcoin",
    "WBTC": "wrapped-bitcoin",
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI": "dai",
    "USDE": "ethena-usde",
    "BNB": "binancecoin",
    "MATIC": "matic-network",
    "AVAX": "avalanche-2",
    "FTM": "fantom",
    "CRO": "crypto-com-chain",
    "xDAI": "xdai",
    "SOL": "solana",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "AAVE": "aave",
    "ARB": "arbitrum",
    "OP": "optimism",
    "JUP": "jupiter-exchange-solana",
    "RAY": "raydium",
    "BONK": "bonk",
}


class PriceService:
    """Service for fetching cryptocurrency prices"""

    def __init__(self):
        """Initialize price service"""
        self.coingecko_api_key = os.getenv("COINGECKO_API_KEY")
        self.cmc_api_key = os.getenv("COINMARKETCAP_API_KEY")
        self.cache: Dict[str, tuple] = {}  # symbol -> (price, timestamp)
        self.cache_duration = timedelta(minutes=5)  # 5 minutes cache

    def _get_cache_key(self, symbol: str) -> Optional[float]:
        """Get price from cache if still valid"""
        if symbol in self.cache:
            price, timestamp = self.cache[symbol]
            if datetime.now() - timestamp < self.cache_duration:
                return price
        return None

    def _set_cache(self, symbol: str, price: float):
        """Set price in cache"""
        self.cache[symbol] = (price, datetime.now())

    def get_price_coingecko(self, symbol: str) -> Optional[float]:
        """
        Get price from CoinGecko

        Args:
            symbol: Token symbol (e.g., "ETH", "BTC")

        Returns:
            Price in USD or None
        """
        # Check cache first
        cached_price = self._get_cache_key(symbol)
        if cached_price is not None:
            return cached_price

        coingecko_id = COINGECKO_IDS.get(symbol.upper())
        if not coingecko_id:
            logger.warning(f"No CoinGecko ID mapping for {symbol}")
            return None

        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coingecko_id,
                "vs_currencies": "usd"
            }

            if self.coingecko_api_key:
                headers = {"x-cg-pro-api-key": self.coingecko_api_key}
            else:
                headers = {}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if coingecko_id in data and "usd" in data[coingecko_id]:
                price = float(data[coingecko_id]["usd"])
                self._set_cache(symbol, price)
                return price

        except Exception as e:
            logger.error(f"Error fetching price from CoinGecko for {symbol}: {e}")

        return None

    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, Optional[float]]:
        """
        Get prices for multiple symbols

        Args:
            symbols: List of token symbols

        Returns:
            Dict mapping symbol to price in USD
        """
        prices = {}
        uncached_symbols = []

        # Check cache first
        for symbol in symbols:
            cached_price = self._get_cache_key(symbol)
            if cached_price is not None:
                prices[symbol] = cached_price
            else:
                uncached_symbols.append(symbol)

        if not uncached_symbols:
            return prices

        # Get CoinGecko IDs for uncached symbols
        coingecko_ids = []
        symbol_to_id = {}
        for symbol in uncached_symbols:
            cg_id = COINGECKO_IDS.get(symbol.upper())
            if cg_id:
                coingecko_ids.append(cg_id)
                symbol_to_id[cg_id] = symbol

        if not coingecko_ids:
            return prices

        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": ",".join(coingecko_ids),
                "vs_currencies": "usd"
            }

            if self.coingecko_api_key:
                headers = {"x-cg-pro-api-key": self.coingecko_api_key}
            else:
                headers = {}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            for cg_id, symbol in symbol_to_id.items():
                if cg_id in data and "usd" in data[cg_id]:
                    price = float(data[cg_id]["usd"])
                    prices[symbol] = price
                    self._set_cache(symbol, price)
                else:
                    prices[symbol] = None

        except Exception as e:
            logger.error(f"Error fetching multiple prices from CoinGecko: {e}")
            for symbol in uncached_symbols:
                if symbol not in prices:
                    prices[symbol] = None

        return prices

    def get_historical_price(self, symbol: str, date: str) -> Optional[float]:
        """
        Get historical price for a specific date

        Args:
            symbol: Token symbol
            date: Date in format "DD-MM-YYYY"

        Returns:
            Historical price in USD or None
        """
        coingecko_id = COINGECKO_IDS.get(symbol.upper())
        if not coingecko_id:
            return None

        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/history"
            params = {"date": date}

            if self.coingecko_api_key:
                headers = {"x-cg-pro-api-key": self.coingecko_api_key}
            else:
                headers = {}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if "market_data" in data and "current_price" in data["market_data"]:
                return float(data["market_data"]["current_price"].get("usd", 0))

        except Exception as e:
            logger.error(f"Error fetching historical price for {symbol}: {e}")

        return None


# Global price service instance
_price_service = None


def get_token_prices(symbols: List[str]) -> Dict[str, Optional[float]]:
    """
    Get current prices for multiple tokens

    Args:
        symbols: List of token symbols

    Returns:
        Dict mapping symbol to price in USD
    """
    global _price_service
    if _price_service is None:
        _price_service = PriceService()

    return _price_service.get_multiple_prices(symbols)


def calculate_portfolio_value(balances: Dict[str, float]) -> Dict[str, any]:
    """
    Calculate total portfolio value in USD

    Args:
        balances: Dict mapping symbol to amount

    Returns:
        Dict with total value and breakdown
    """
    global _price_service
    if _price_service is None:
        _price_service = PriceService()

    symbols = list(balances.keys())
    prices = _price_service.get_multiple_prices(symbols)

    portfolio_breakdown = []
    total_value = 0.0

    for symbol, amount in balances.items():
        price = prices.get(symbol)
        if price is not None:
            value = amount * price
            total_value += value
            portfolio_breakdown.append({
                "symbol": symbol,
                "amount": amount,
                "price_usd": price,
                "value_usd": value
            })

    return {
        "total_value_usd": total_value,
        "breakdown": portfolio_breakdown,
        "prices_fetched_at": datetime.now().isoformat()
    }
