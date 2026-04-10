"""FastAPI publisher example — gate AI agents behind Xenarch payments.

Demonstrates both site-wide middleware and per-route decorator patterns.

Usage:
    uvicorn main:app --reload
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from xenarch.decorator import require_payment
from xenarch.middleware import XenarchMiddleware

load_dotenv()

SITE_TOKEN = os.environ["XENARCH_SITE_TOKEN"]
SITE_ID = os.environ["XENARCH_SITE_ID"]
ACCESS_TOKEN_SECRET = os.environ["XENARCH_ACCESS_TOKEN_SECRET"]

app = FastAPI(title="Xenarch Publisher Example")

# Pattern 1: Site-wide middleware
# Gates all bot requests except excluded paths.
# Comment this out if you only want per-route gating.
app.add_middleware(
    XenarchMiddleware,
    site_token=SITE_TOKEN,
    site_id=SITE_ID,
    access_token_secret=ACCESS_TOKEN_SECRET,
    excluded_paths={"/healthz", "/docs", "/openapi.json", "/"},
)

# Pattern 2: Per-route decorator
# Use this for selective gating on specific routes.
gate = require_payment(
    site_token=SITE_TOKEN,
    site_id=SITE_ID,
    access_token_secret=ACCESS_TOKEN_SECRET,
)


@app.get("/")
async def home():
    """Free route — not gated."""
    return {"message": "Welcome! This content is free for everyone."}


@app.get("/healthz")
async def health():
    """Health check — excluded from gating."""
    return {"status": "ok"}


@app.get("/articles")
async def articles():
    """Gated by the site-wide middleware (bot requests get 402)."""
    return {
        "articles": [
            {"title": "Understanding AI Payments", "id": 1},
            {"title": "Micropayments at Scale", "id": 2},
        ]
    }


@app.get("/premium")
@gate
async def premium(request: Request):
    """Gated by the per-route decorator (bot requests get 402)."""
    return {"content": "This is premium content worth paying for."}
