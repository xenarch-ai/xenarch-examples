# FastAPI Publisher — Xenarch Middleware

Charge AI agents for accessing your API or content. Shows two integration patterns: site-wide middleware and per-route decorator.

## Prerequisites

- Python 3.10+
- A Xenarch publisher account with a registered site
- Your site token, site ID, and access token secret (from Xenarch CLI or dashboard)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your publisher credentials:

```
XENARCH_SITE_TOKEN=st_your_site_token
XENARCH_SITE_ID=your-site-uuid
XENARCH_ACCESS_TOKEN_SECRET=your_secret
```

## Run

```bash
uvicorn main:app --reload
```

## How It Works

The middleware intercepts requests and checks:

1. **Is this a bot?** — Checks the User-Agent header
2. **Does it have a valid token?** — Checks the `Authorization: Bearer` header
3. **If bot without token** — Returns HTTP 402 with payment gate details
4. **If human or valid token** — Passes through normally

```
Human request     → passes through (zero impact)
Bot + valid token → passes through
Bot + no token    → HTTP 402 { gate_id, price_usd, splitter, ... }
```

## Integration Patterns

### Pattern 1: Site-wide middleware

Gates all routes (except excluded paths):

```python
from xenarch.middleware import XenarchMiddleware

app.add_middleware(
    XenarchMiddleware,
    site_token="st_...",
    site_id="...",
    access_token_secret="...",
    excluded_paths={"/healthz", "/docs"},
)
```

### Pattern 2: Per-route decorator

Gates individual routes:

```python
from xenarch.decorator import require_payment

gate = require_payment(
    site_token="st_...",
    site_id="...",
    access_token_secret="...",
)

@app.get("/premium")
@gate
async def premium(request: Request):
    return {"content": "premium data"}
```

## Testing

```bash
# Human request — passes through
curl http://localhost:8000/

# Bot request without token — returns 402
curl -H "User-Agent: GPTBot/1.0" http://localhost:8000/premium

# Bot request with valid access token — passes through
curl -H "User-Agent: GPTBot/1.0" \
     -H "Authorization: Bearer <access_token>" \
     http://localhost:8000/premium
```

## Expected Responses

**Free route (human or bot):**
```json
{"message": "Welcome! This content is free for everyone."}
```

**Gated route (bot without token):**
```
HTTP 402 Payment Required
{"gate_id": "...", "price_usd": "0.003", "splitter": "0x...", ...}
```

**Gated route (bot with valid token):**
```json
{"content": "This is premium content worth paying for."}
```
