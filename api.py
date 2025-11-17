#!/usr/bin/env python3
"""FastAPI REST API for Universal On-Chain Balance Tracker"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional, List

from app.validators import detect_address_type, validate_evm_address, validate_solana_address
from app.chains.evm import get_all_evm_balances, EVM_NETWORKS
from app.chains.solana import get_solana_balances
from app.models import BalanceResponse, ErrorResponse
from app.config import SOLANA_CONFIG

# Initialize FastAPI app
app = FastAPI(
    title="Universal On-Chain Balance Tracker",
    description="REST API for checking wallet balances across multiple blockchains (EVM + Solana)",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Universal On-Chain Balance Tracker"}


@app.get("/networks", tags=["Info"])
async def get_supported_networks():
    """Get list of supported networks"""
    evm_networks = [
        {
            "key": key,
            "name": config["name"],
            "chain_id": config["chain_id"],
            "native_token": config["native_token"],
            "type": "EVM"
        }
        for key, config in EVM_NETWORKS.items()
    ]

    solana_network = {
        "key": "solana",
        "name": SOLANA_CONFIG["name"],
        "chain_id": None,
        "native_token": SOLANA_CONFIG["native_token"],
        "type": "Solana"
    }

    return {
        "total_networks": len(evm_networks) + 1,
        "networks": evm_networks + [solana_network]
    }


@app.get("/balances", response_model=BalanceResponse, tags=["Balances"])
async def get_balances(
    address: str = Query(..., description="Wallet address (EVM or Solana)"),
    networks: Optional[str] = Query(None, description="Comma-separated list of networks (e.g., 'ethereum,polygon,solana')")
):
    """
    Get wallet balances across all supported networks or specific networks

    **Parameters:**
    - **address**: Wallet address (EVM format: 0x... or Solana format: base58)
    - **networks**: (Optional) Comma-separated list of networks to check

    **Examples:**
    - `/balances?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`
    - `/balances?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&networks=ethereum,polygon`
    - `/balances?address=9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM`
    """
    try:
        # Detect address type
        address_type = detect_address_type(address)

        if address_type == "unknown":
            raise HTTPException(
                status_code=400,
                detail="Invalid address format. Must be valid EVM (0x...) or Solana (base58) address."
            )

        all_balances = []

        # Parse network filter
        network_filter = None
        if networks:
            network_filter = [n.strip().lower() for n in networks.split(",")]

        # Get EVM balances
        if address_type == "evm":
            is_valid, result = validate_evm_address(address)
            if not is_valid:
                raise HTTPException(status_code=400, detail=f"Invalid EVM address: {result}")

            address = result  # Use checksum address

            # Get balances for specific networks or all
            if network_filter:
                for network_key in EVM_NETWORKS.keys():
                    if network_key in network_filter or EVM_NETWORKS[network_key]["name"].lower() in network_filter:
                        from app.chains.evm import EVMClient
                        client = EVMClient(network_key)
                        balance = client.get_all_balances(address)
                        all_balances.append(balance)
            else:
                evm_balances = get_all_evm_balances(address)
                all_balances.extend(evm_balances)

        # Get Solana balances
        if address_type == "solana":
            is_valid, result = validate_solana_address(address)
            if not is_valid:
                raise HTTPException(status_code=400, detail=f"Invalid Solana address: {result}")

            # Check if Solana is in filter or no filter specified
            if not network_filter or "solana" in network_filter:
                solana_balance = get_solana_balances(address)
                all_balances.append(solana_balance)

        return BalanceResponse(
            address=address,
            networks=all_balances,
            total_networks_checked=len(all_balances),
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/validate", tags=["Validation"])
async def validate_address(address: str = Query(..., description="Address to validate")):
    """
    Validate an address and detect its type

    **Parameters:**
    - **address**: Address to validate

    **Returns:**
    - Address type (evm, solana, or unknown)
    - Validation status
    - Checksum address (for EVM)
    """
    address_type = detect_address_type(address)

    if address_type == "evm":
        is_valid, result = validate_evm_address(address)
        return {
            "valid": is_valid,
            "type": "evm",
            "checksum_address": result if is_valid else None,
            "message": result if is_valid else "Invalid EVM address"
        }
    elif address_type == "solana":
        is_valid, result = validate_solana_address(address)
        return {
            "valid": is_valid,
            "type": "solana",
            "address": result if is_valid else None,
            "message": result if is_valid else "Invalid Solana address"
        }
    else:
        return {
            "valid": False,
            "type": "unknown",
            "message": "Unknown address format"
        }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "details": f"The requested endpoint does not exist. Visit / for API documentation."
        }
    )


def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Start the FastAPI server"""
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Universal On-Chain Balance Tracker API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    print(f"Starting Universal On-Chain Balance Tracker API on {args.host}:{args.port}")
    print(f"Documentation available at http://{args.host}:{args.port}/")

    start_server(host=args.host, port=args.port, reload=args.reload)
