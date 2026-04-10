# Python Agent — Basic

Minimal Python example: discover a payment gate, pay with USDC on Base, and get an access token.

## Prerequisites

- Python 3.10+
- A wallet with USDC on Base (or Base Sepolia for testnet)
- Small amount of ETH on Base for gas fees

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your wallet private key:

```
XENARCH_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
```

For testnet, also set:

```
XENARCH_NETWORK=base-sepolia
XENARCH_RPC_URL=https://sepolia.base.org
```

## Run

```bash
python main.py https://example.com
```

Replace `https://example.com` with any Xenarch-gated URL.

## What It Does

1. **Checks the gate** — calls the Xenarch API to see if the URL requires payment
2. **Executes payment** — sends USDC through the splitter contract on Base
3. **Verifies and gets token** — confirms payment with the platform, receives a time-limited access token
4. **Fetches content** — re-requests the URL with the access token

## Expected Output

```
Checking gate for: https://example.com
Gate found! Price: $0.003 (USDC on base)

Executing payment...
Payment confirmed!
  TX: 0xabc123...
  Block: 28451023

Verifying payment...
Access token received (expires: 2026-04-10T15:05:00Z)

Fetching gated content...
Content retrieved successfully (1,234 bytes)
```
