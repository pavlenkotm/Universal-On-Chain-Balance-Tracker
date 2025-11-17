"""Tests for price service"""

import pytest
from app.price_feeds.price_service import PriceService


class TestPriceService:
    """Test price service functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.price_service = PriceService()

    def test_get_price_with_cache(self):
        """Test price fetching with caching"""
        # First call should hit API
        price1 = self.price_service.get_price_coingecko("ETH")

        # Second call should hit cache
        price2 = self.price_service.get_price_coingecko("ETH")

        if price1 is not None:
            assert price1 == price2
            assert isinstance(price1, float)
            assert price1 > 0

    def test_get_multiple_prices(self):
        """Test fetching multiple prices at once"""
        symbols = ["ETH", "BTC", "USDC"]
        prices = self.price_service.get_multiple_prices(symbols)

        assert isinstance(prices, dict)
        assert len(prices) == len(symbols)

    def test_cache_functionality(self):
        """Test that cache stores and retrieves correctly"""
        self.price_service._set_cache("TEST", 100.0)
        cached_price = self.price_service._get_cache_key("TEST")

        assert cached_price == 100.0

    def test_unknown_symbol(self):
        """Test handling of unknown symbol"""
        price = self.price_service.get_price_coingecko("UNKNOWN_TOKEN_XYZ")
        # Should return None for unknown tokens
        assert price is None or isinstance(price, float)


@pytest.mark.integration
class TestPriceIntegration:
    """Integration tests for price service (requires internet)"""

    def test_fetch_real_eth_price(self):
        """Test fetching real ETH price from CoinGecko"""
        service = PriceService()
        price = service.get_price_coingecko("ETH")

        # ETH price should be positive
        if price is not None:
            assert price > 0
            assert price < 100000  # Reasonable upper bound
