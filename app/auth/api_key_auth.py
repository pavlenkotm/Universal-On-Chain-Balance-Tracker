"""API Key authentication"""

import secrets
import hashlib
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# API Key header scheme
APIKeyHeader = APIKeyHeader(name="X-API-Key", auto_error=False)


def hash_api_key(key: str) -> str:
    """Hash API key for storage"""
    return hashlib.sha256(key.encode()).hexdigest()


def generate_api_key() -> tuple[str, str]:
    """
    Generate new API key

    Returns:
        Tuple of (plain_key, hashed_key)
    """
    plain_key = f"bt_{secrets.token_urlsafe(32)}"
    hashed_key = hash_api_key(plain_key)
    return plain_key, hashed_key


def create_api_key(db: Session, name: str, user_id: str = None, rate_limit: int = 1000) -> str:
    """
    Create new API key in database

    Args:
        db: Database session
        name: Key name/description
        user_id: Optional user ID
        rate_limit: Requests per hour

    Returns:
        Plain text API key (only shown once)
    """
    from ..database.models import APIKey

    plain_key, hashed_key = generate_api_key()

    api_key = APIKey(
        key_hash=hashed_key,
        name=name,
        user_id=user_id,
        rate_limit=rate_limit,
        is_active=True
    )

    db.add(api_key)
    db.commit()

    logger.info(f"API key created: {name}")

    return plain_key


def verify_api_key(api_key: str = Security(APIKeyHeader), db: Session = None) -> dict:
    """
    Verify API key from request header

    Args:
        api_key: API key from header
        db: Database session

    Returns:
        API key info dict

    Raises:
        HTTPException: If API key is invalid or inactive
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )

    if not db:
        # If no DB available, allow pass-through for development
        logger.warning("API key verification skipped (no database)")
        return {"authenticated": False, "rate_limit": 1000}

    from ..database.models import APIKey

    hashed_key = hash_api_key(api_key)

    key_record = db.query(APIKey).filter(
        APIKey.key_hash == hashed_key,
        APIKey.is_active == True
    ).first()

    if not key_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key"
        )

    # Update last used timestamp
    key_record.last_used = datetime.now()
    db.commit()

    return {
        "authenticated": True,
        "key_id": key_record.id,
        "name": key_record.name,
        "user_id": key_record.user_id,
        "rate_limit": key_record.rate_limit
    }
