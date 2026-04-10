# Xenarch Examples

Working examples for integrating with the [Xenarch](https://xenarch.com) payment network. Each example is self-contained with its own README and copy-paste instructions.

## For AI Agents (pay for content)

| Example | Description |
|---------|-------------|
| [python-agent-basic](python-agent-basic/) | Raw Python SDK — check gate, pay, verify access |
| [langchain-agent](langchain-agent/) | LangChain agent that autonomously pays for gated content |
| [crewai-agent](crewai-agent/) | CrewAI crew with Xenarch payment tools |
| [mcp-claude-desktop](mcp-claude-desktop/) | Setup guide for Claude Desktop and Claude Code |

## For Publishers (charge AI agents)

| Example | Description |
|---------|-------------|
| [fastapi-publisher](fastapi-publisher/) | FastAPI middleware and per-route decorator |

## Prerequisites

- Python 3.10+ (for Python examples)
- A funded wallet on Base (USDC + small ETH for gas)
- For testnet: use `base-sepolia` network with test USDC

## Quick Start

Every example follows the same pattern:

```bash
cd <example-dir>
pip install -r requirements.txt
cp .env.example .env   # edit with your keys
python main.py
```

## How Xenarch Works

```
1. Discover    Agent checks if a URL has a payment gate
2. Pay         Agent sends USDC on Base via the splitter contract
3. Access      Agent gets a time-limited access token
```

No API keys. No signup. Agents pay publishers directly on-chain.

## Resources

- [xenarch-mcp](https://github.com/xenarch-ai/xenarch-mcp) — MCP server for AI agents
- [xenarch Python SDK](https://pypi.org/project/xenarch/) — `pip install xenarch`
- [pay.json spec](https://github.com/xenarch-ai/pay-json) — Machine-readable pricing standard
- [API docs](https://docs.xenarch.dev) — OpenAPI reference

## License

MIT
