#!/usr/bin/env python3
"""CLI interface for Universal On-Chain Balance Tracker"""

import argparse
import json
import sys
from app.validators import validate_evm_address, validate_solana_address, detect_address_type
from app.chains.evm import get_all_evm_balances
from app.chains.solana import get_solana_balances
from app.models import BalanceResponse


def format_output(response: BalanceResponse, format_type: str = "json") -> str:
    """Format output for display"""
    if format_type == "json":
        return response.model_dump_json(indent=2)

    # Pretty text format
    output_lines = []
    output_lines.append(f"\n{'='*80}")
    output_lines.append(f"BALANCE TRACKER RESULTS FOR: {response.address}")
    output_lines.append(f"{'='*80}\n")

    for network in response.networks:
        output_lines.append(f"\n{network.network} ({network.native_token})")
        output_lines.append("-" * 40)
        output_lines.append(f"Native Balance: {network.native_balance_formatted} {network.native_token}")

        if network.tokens:
            output_lines.append(f"\nTokens ({len(network.tokens)}):")
            for token in network.tokens:
                output_lines.append(f"  • {token.symbol}: {token.balance_formatted}")
        else:
            output_lines.append("\nNo tokens with balance found")

        if network.explorer_url:
            output_lines.append(f"\nExplorer: {network.explorer_url}")
        output_lines.append("")

    output_lines.append(f"\n{'='*80}")
    output_lines.append(f"Total Networks Checked: {response.total_networks_checked}")
    output_lines.append(f"{'='*80}\n")

    return "\n".join(output_lines)


def get_balances(address: str) -> BalanceResponse:
    """
    Get balances for an address across all supported networks

    Args:
        address: Wallet address

    Returns:
        BalanceResponse object
    """
    # Detect address type
    address_type = detect_address_type(address)

    if address_type == "unknown":
        return BalanceResponse(
            address=address,
            networks=[],
            total_networks_checked=0,
            success=False,
            error="Invalid address format. Must be valid EVM or Solana address."
        )

    all_balances = []

    # Get EVM balances
    if address_type == "evm":
        is_valid, result = validate_evm_address(address)
        if is_valid:
            address = result  # Use checksum address
            evm_balances = get_all_evm_balances(address)
            all_balances.extend(evm_balances)

    # Get Solana balances
    if address_type == "solana":
        is_valid, result = validate_solana_address(address)
        if is_valid:
            solana_balance = get_solana_balances(address)
            all_balances.append(solana_balance)

    return BalanceResponse(
        address=address,
        networks=all_balances,
        total_networks_checked=len(all_balances),
        success=True
    )


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Universal On-Chain Balance Tracker - Check balances across multiple blockchains",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check EVM address balances
  python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

  # Check Solana address balances
  python main.py --address 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM

  # Output in JSON format
  python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --format json

  # Output in pretty text format
  python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --format text
        """
    )

    parser.add_argument(
        "--address",
        "-a",
        required=True,
        help="Wallet address (EVM or Solana)"
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--networks",
        "-n",
        nargs="+",
        help="Specific networks to check (e.g., ethereum polygon solana)"
    )

    args = parser.parse_args()

    try:
        # Get balances
        response = get_balances(args.address)

        # Filter networks if specified
        if args.networks:
            networks_lower = [n.lower() for n in args.networks]
            response.networks = [
                net for net in response.networks
                if net.network.lower() in networks_lower or
                   any(keyword in net.network.lower() for keyword in networks_lower)
            ]
            response.total_networks_checked = len(response.networks)

        # Output results
        output = format_output(response, args.format)
        print(output)

        # Exit with appropriate code
        sys.exit(0 if response.success else 1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
