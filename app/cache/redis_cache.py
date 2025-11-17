"""Redis caching implementation"""

import os
import json
import redis
from typing import Optional, Any
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache wrapper for balance data"""

    def __init__(self):
        """Initialize Redis connection"""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

        try:
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True
            )
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.warning(f"Redis not available, caching disabled: {e}")
            self.redis_client = None
            self.enabled = False

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if not self.enabled:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")

        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 300 = 5 minutes)
        """
        if not self.enabled:
            return

        try:
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Error setting cache: {e}")

    def delete(self, key: str):
        """
        Delete value from cache

        Args:
            key: Cache key
        """
        if not self.enabled:
            return

        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")

    def clear_pattern(self, pattern: str):
        """
        Clear all keys matching pattern

        Args:
            pattern: Pattern to match (e.g., "balance:*")
        """
        if not self.enabled:
            return

        try:
            cursor = 0
            while True:
                cursor, keys = self.redis_client.scan(cursor, match=pattern, count=100)
                if keys:
                    self.redis_client.delete(*keys)
                if cursor == 0:
                    break
        except Exception as e:
            logger.error(f"Error clearing cache pattern: {e}")

    def get_balance_cache_key(self, address: str, network: str) -> str:
        """Generate cache key for balance data"""
        return f"balance:{network}:{address.lower()}"

    def get_price_cache_key(self, symbol: str) -> str:
        """Generate cache key for price data"""
        return f"price:{symbol.upper()}"

    def cache_balance(self, address: str, network: str, data: dict, ttl: int = 60):
        """Cache balance data for an address on a network"""
        key = self.get_balance_cache_key(address, network)
        self.set(key, data, ttl)

    def get_cached_balance(self, address: str, network: str) -> Optional[dict]:
        """Get cached balance data"""
        key = self.get_balance_cache_key(address, network)
        return self.get(key)


# Global cache instance
_cache = None


def get_cache() -> RedisCache:
    """Get global cache instance"""
    global _cache
    if _cache is None:
        _cache = RedisCache()
    return _cache
