# LangChain Agent with Xenarch Payments

A LangChain agent that can autonomously discover payment gates, pay for content, and access gated resources.

## Prerequisites

- Python 3.10+
- A wallet with USDC on Base (or Base Sepolia for testnet)
- An OpenAI API key (or any LangChain-compatible LLM)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```
XENARCH_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
OPENAI_API_KEY=sk-...
```

## Run

```bash
python main.py
```

## What It Does

Creates a LangChain agent with three Xenarch tools:

| Tool | Description |
|------|-------------|
| `xenarch_check_gate` | Check if a URL has a payment gate |
| `xenarch_pay` | Pay for gated content with USDC |
| `xenarch_get_history` | View past payments |

The agent receives a prompt and autonomously decides when to check gates, pay, and retrieve content.

## Example Interaction

```
Prompt: "Check if example.com has a paywall. If it does, pay for access."

Agent thinking: I'll check if example.com has a Xenarch payment gate...
Agent action: xenarch_check_gate("example.com")
Agent observation: {"gated": true, "price_usd": "0.003", ...}
Agent thinking: There's a gate at $0.003. I'll pay for access...
Agent action: xenarch_pay("example.com")
Agent observation: {"success": true, "access_token": "eyJ...", ...}
Agent: I've paid $0.003 USDC for access to example.com. Here's your access token: eyJ...
```

## Customization

Swap the LLM by changing the model in `main.py`:

```python
# Use Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

# Use a local model via Ollama
from langchain_community.llms import Ollama
llm = Ollama(model="llama3")
```
