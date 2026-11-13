"""Environment-based configuration."""

import os

MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("GOLD_SILVER_MCP_PORT", "8061"))
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "http").lower()

API_BASE_URL = os.getenv(
    "GOLD_SILVER_API_BASE_URL", "https://alyawmgold.com/api/v1"
).rstrip("/")
API_TIMEOUT = float(os.getenv("GOLD_SILVER_API_TIMEOUT", "15"))

CACHE_TTL_SPOT = int(os.getenv("GOLD_SILVER_CACHE_TTL_SPOT", "30"))
CACHE_TTL_HISTORY = int(os.getenv("GOLD_SILVER_CACHE_TTL_HISTORY", "300"))
CACHE_TTL_MARKETS = int(os.getenv("GOLD_SILVER_CACHE_TTL_MARKETS", "1800"))
