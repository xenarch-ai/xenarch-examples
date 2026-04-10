# CrewAI Agent with Xenarch Payments

A CrewAI crew that can research gated content and autonomously pay for access.

## Prerequisites

- Python 3.10+
- A wallet with USDC on Base (or Base Sepolia for testnet)
- An OpenAI API key (or any CrewAI-compatible LLM)

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

Creates a CrewAI agent ("Research Agent") with three Xenarch tools:

| Tool | Description |
|------|-------------|
| `xenarch_check_gate` | Check if a URL has a payment gate |
| `xenarch_pay` | Pay for gated content with USDC |
| `xenarch_get_history` | View past payments |

The crew assigns a research task that requires paying for gated content, and the agent handles the payment flow autonomously.

## Example Output

```
[Research Agent] Checking if example.com has a payment gate...
[Research Agent] Gate found — $0.003 USDC. Paying...
[Research Agent] Payment successful. Access token received.
[Research Agent] Research complete.

Final result: Successfully accessed gated content on example.com.
Paid $0.003 USDC (tx: 0xabc123...).
```
