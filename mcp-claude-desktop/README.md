# Xenarch MCP — Claude Desktop & Claude Code Setup

Step-by-step guide to adding Xenarch payment tools to Claude Desktop or Claude Code. No code required — just configuration.

## Prerequisites

- Node.js 18+
- A wallet with USDC on Base (or Base Sepolia for testnet)
- Claude Desktop or Claude Code installed

## Step 1: Create Your Wallet

If you already have a wallet, skip to Step 2.

```bash
mkdir -p ~/.xenarch
cat > ~/.xenarch/wallet.json << 'EOF'
{
  "privateKey": "0xYOUR_PRIVATE_KEY"
}
EOF
chmod 600 ~/.xenarch/wallet.json
```

The MCP server will auto-generate a wallet on first run if none exists. You'll need to fund it with USDC on Base before making payments.

## Step 2a: Add to Claude Code

```bash
claude mcp add xenarch -- npx @xenarch/agent-mcp
```

That's it. The three Xenarch tools are now available in Claude Code.

## Step 2b: Add to Claude Desktop

Edit your Claude Desktop configuration file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the Xenarch server:

```json
{
  "mcpServers": {
    "xenarch": {
      "command": "npx",
      "args": ["@xenarch/agent-mcp"],
      "env": {
        "XENARCH_PRIVATE_KEY": "0xYOUR_PRIVATE_KEY"
      }
    }
  }
}
```

A complete example config is in [`claude_desktop_config.json`](claude_desktop_config.json).

Restart Claude Desktop to pick up the change.

## Step 3: Test It

Try these prompts in Claude:

- "Check if example.com has a Xenarch payment gate"
- "Pay for access to example.com and show me the content"
- "Show my Xenarch payment history"

## Available Tools

| Tool | Description |
|------|-------------|
| `xenarch_check_gate` | Check if a URL/domain has a payment gate |
| `xenarch_pay` | Pay for gated content with USDC on Base |
| `xenarch_get_history` | View past payments |

## Configuration

Set environment variables to customize behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| `XENARCH_PRIVATE_KEY` | — | Wallet private key |
| `XENARCH_NETWORK` | `base` | `base` or `base-sepolia` |
| `XENARCH_RPC_URL` | `https://mainnet.base.org` | Base RPC endpoint |
| `XENARCH_AUTO_APPROVE_MAX` | — | Max USD to auto-approve |

## Testnet Setup

For testing without real funds, use Base Sepolia:

```json
{
  "mcpServers": {
    "xenarch": {
      "command": "npx",
      "args": ["@xenarch/agent-mcp"],
      "env": {
        "XENARCH_PRIVATE_KEY": "0xYOUR_PRIVATE_KEY",
        "XENARCH_NETWORK": "base-sepolia",
        "XENARCH_RPC_URL": "https://sepolia.base.org"
      }
    }
  }
}
```

## Troubleshooting

**"No wallet configured"** — Set `XENARCH_PRIVATE_KEY` in the env block, or create `~/.xenarch/wallet.json`.

**"Insufficient USDC"** — Fund your wallet with USDC on Base. You also need a small amount of ETH for gas.

**Tools not appearing** — Restart Claude Desktop. Check that `npx @xenarch/agent-mcp` runs without errors in your terminal.
