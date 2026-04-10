"""Minimal Xenarch agent: check gate, pay, get content.

Usage:
    python main.py https://example.com
"""

import sys

import httpx
from dotenv import load_dotenv

from xenarch.agent_client import check_gate, verify_payment
from xenarch.payment import execute_payment
from xenarch.wallet import load_wallet_or_create

load_dotenv()


def main(url: str) -> None:
    wallet = load_wallet_or_create()
    print(f"Wallet: {wallet.address}")
    print(f"Network: {wallet.network}\n")

    # 1. Check if the URL has a payment gate
    print(f"Checking gate for: {url}")
    gate = check_gate(url)
    if not gate:
        print("No Xenarch gate found — content is free.")
        return

    print(f"Gate found! Price: ${gate.price_usd} ({gate.asset} on {gate.network})\n")

    # 2. Execute on-chain USDC payment
    print("Executing payment...")
    result = execute_payment(
        wallet=wallet,
        splitter_address=gate.splitter,
        collector_address=gate.collector,
        price_usd=gate.price_usd,
    )
    print(f"Payment confirmed!")
    print(f"  TX: {result.tx_hash}")
    print(f"  Block: {result.block_number}\n")

    # 3. Verify payment and get access token
    print("Verifying payment...")
    verification = verify_payment(gate.verify_url, result.tx_hash)
    access_token = verification["access_token"]
    expires_at = verification["expires_at"]
    print(f"Access token received (expires: {expires_at})\n")

    # 4. Fetch the gated content with the access token
    print("Fetching gated content...")
    resp = httpx.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "xenarch-example/1.0",
        },
    )
    print(f"Content retrieved successfully ({len(resp.content):,} bytes)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        print("Example: python main.py https://example.com/premium-article")
        sys.exit(1)
    main(sys.argv[1])
