"""Prometheus metrics for monitoring"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

balance_requests_total = Counter(
    'balance_requests_total',
    'Total balance check requests',
    ['network', 'status']
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

rpc_requests_total = Counter(
    'rpc_requests_total',
    'Total RPC requests to blockchain nodes',
    ['network', 'status']
)

rpc_request_duration_seconds = Histogram(
    'rpc_request_duration_seconds',
    'RPC request duration in seconds',
    ['network']
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics"""

    async def dispatch(self, request: Request, call_next):
        # Skip metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)

        active_connections.inc()
        start_time = time.time()

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Record metrics
            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()

            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)

            return response

        except Exception as e:
            duration = time.time() - start_time

            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()

            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)

            raise

        finally:
            active_connections.dec()


def metrics_middleware():
    """Get metrics middleware instance"""
    return MetricsMiddleware


def get_metrics():
    """Get Prometheus metrics in text format"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# Helper functions to record custom metrics
def record_balance_request(network: str, success: bool):
    """Record a balance check request"""
    status = "success" if success else "error"
    balance_requests_total.labels(network=network, status=status).inc()


def record_cache_hit(cache_type: str = "balance"):
    """Record a cache hit"""
    cache_hits_total.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str = "balance"):
    """Record a cache miss"""
    cache_misses_total.labels(cache_type=cache_type).inc()


def record_rpc_request(network: str, duration: float, success: bool):
    """Record an RPC request"""
    status = "success" if success else "error"
    rpc_requests_total.labels(network=network, status=status).inc()
    rpc_request_duration_seconds.labels(network=network).observe(duration)
