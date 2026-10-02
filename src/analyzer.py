"""Analyze an EVM wallet using a JSON-RPC endpoint."""

import argparse
import json
import os
import sys
from decimal import Decimal
from typing import Any

from web3 import Web3


def analyze_wallet(address: str, rpc_url: str) -> dict[str, Any]:
    """Return basic on-chain data for an address using the given RPC URL."""
    if not Web3.is_address(address):
        raise ValueError("Invalid EVM address")

    checksum_address = Web3.to_checksum_address(address)
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Could not connect to RPC endpoint")

    balance_eth = Web3.from_wei(web3.eth.get_balance(checksum_address), "ether")
    return {
        "address": checksum_address,
        "chain_id": web3.eth.chain_id,
        "balance_eth": str(Decimal(balance_eth)),
        "nonce": web3.eth.get_transaction_count(checksum_address),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze an EVM wallet using an RPC endpoint.")
    parser.add_argument("address", help="EVM wallet address")
    parser.add_argument("--rpc", default=os.environ.get("RPC_URL"), help="EVM JSON-RPC endpoint (or set RPC_URL)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.rpc:
        parser.error("provide --rpc or set the RPC_URL environment variable")
    try:
        result = analyze_wallet(args.address, args.rpc)
    except (ValueError, ConnectionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"RPC request failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
