"""Database models for PostgreSQL"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class BalanceSnapshot(Base):
    """Model for storing historical balance snapshots"""
    __tablename__ = "balance_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100), nullable=False, index=True)
    network = Column(String(50), nullable=False)
    snapshot_data = Column(JSON, nullable=False)  # Full balance data as JSON
    total_value_usd = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index('idx_address_network_created', 'address', 'network', 'created_at'),
    )


class UserAlert(Base):
    """Model for user-configured price/balance alerts"""
    __tablename__ = "user_alerts"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)  # 'balance_above', 'balance_below', 'price_above', 'price_below'
    network = Column(String(50))
    token_symbol = Column(String(20))
    threshold = Column(Float, nullable=False)
    webhook_url = Column(Text)
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_active_alerts', 'is_active', 'address'),
    )


class APIKey(Base):
    """Model for API key authentication"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    user_id = Column(String(100), index=True)
    rate_limit = Column(Integer, default=1000)  # Requests per hour
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True))

    __table_args__ = (
        Index('idx_active_keys', 'is_active', 'key_hash'),
    )


class WebhookLog(Base):
    """Model for webhook delivery logs"""
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    webhook_url = Column(Text, nullable=False)
    payload = Column(JSON)
    status_code = Column(Integer)
    response = Column(Text)
    success = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class BatchRequest(Base):
    """Model for batch processing requests"""
    __tablename__ = "batch_requests"

    id = Column(Integer, primary_key=True, index=True)
    addresses = Column(JSON, nullable=False)  # List of addresses
    status = Column(String(20), default='pending')  # pending, processing, completed, failed
    result = Column(JSON)  # Results when completed
    error = Column(Text)  # Error message if failed
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index('idx_status_created', 'status', 'created_at'),
    )
