"""Gold and Silver MCP Server using the public AlyawmGold API."""

import logging
import time
from typing import Optional

import httpx
from fastmcp import FastMCP

from config import (
    API_BASE_URL,
    API_TIMEOUT,
    CACHE_TTL_HISTORY,
    CACHE_TTL_MARKETS,
    CACHE_TTL_SPOT,
    MCP_HOST,
    MCP_PORT,
    MCP_TRANSPORT,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gold-silver-mcp")
mcp = FastMCP("Gold and Silver MCP Server")
_cache = {}


def api_get(path: str, params: Optional[dict] = None, ttl: int = 30):
    """GET JSON from the upstream API with a small in-memory cache."""
    import json

    key = f"{path}:{json.dumps(params or {}, sort_keys=True)}"
    now = time.monotonic()
    cached = _cache.get(key)
    if cached and now - cached["time"] < ttl:
        return cached["data"]

    try:
        response = httpx.get(
            f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}",
            params=params,
            timeout=API_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.TimeoutException as exc:
        raise RuntimeError("Metals API request timed out") from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Metals API returned HTTP {exc.response.status_code}: "
            f"{exc.response.text[:300]}"
        ) from exc
    except httpx.RequestError as exc:
        raise RuntimeError(f"Metals API connection error: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("Metals API returned invalid JSON") from exc

    _cache[key] = {"time": now, "data": data}
    return data


@mcp.tool
def get_today_gold_price(country: str = "AE") -> dict:
    """Get the latest gold reference price for a country. Defaults to AE (UAE)."""
    data = api_get("spot/latest", {"country": country.upper()}, CACHE_TTL_SPOT)
    gold = (data.get("metals") or {}).get("gold")
    if gold is None:
        return {"available": False, "metal": "gold", "country": country.upper()}
    return {
        "available": True,
        "metal": "gold",
        "country": data.get("country", country.upper()),
        "price": gold,
        "source": "AlyawmGold",
        "disclaimer": "Indicative reference price; excludes dealer premiums, making charges and taxes.",
    }


@mcp.tool
def get_today_silver_price(country: str = "AE") -> dict:
    """Get the latest silver reference price for a country. Defaults to AE (UAE)."""
    data = api_get("spot/latest", {"country": country.upper()}, CACHE_TTL_SPOT)
    silver = (data.get("metals") or {}).get("silver")
    if silver is None:
        return {"available": False, "metal": "silver", "country": country.upper()}
    return {
        "available": True,
        "metal": "silver",
        "country": data.get("country", country.upper()),
        "price": silver,
        "source": "AlyawmGold",
        "disclaimer": "Indicative reference price; excludes dealer premiums and taxes.",
    }


@mcp.tool
def get_today_metals_prices(country: str = "AE") -> dict:
    """Get current gold and silver reference prices together."""
    data = api_get("spot/latest", {"country": country.upper()}, CACHE_TTL_SPOT)
    metals = data.get("metals") or {}
    return {
        "country": data.get("country", country.upper()),
        "gold": metals.get("gold"),
        "silver": metals.get("silver"),
        "timestamp": data.get("quoteRecordedAtUtc"),
        "source": "AlyawmGold",
        "disclaimer": "Indicative reference prices; exclude dealer premiums, making charges and taxes.",
    }


@mcp.tool
def get_supported_markets() -> dict:
    """List supported markets and currencies."""
    return api_get("markets", ttl=CACHE_TTL_MARKETS)


@mcp.tool
def get_metal_price_history(
    metal: str = "XAU",
    interval: str = "daily",
    limit: int = 30,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> dict:
    """Get historical gold (XAU) or silver (XAG) prices.

    Args:
        metal: XAU/gold or XAG/silver.
        interval: daily, monthly, or yearly.
        limit: Number of records, from 1 to 1000.
        from_date: Optional start date, YYYY-MM-DD.
        to_date: Optional end date, YYYY-MM-DD.
    """
    metal = metal.strip().upper()
    if metal in ("GOLD", "XAU"):
        metal = "XAU"
    elif metal in ("SILVER", "XAG"):
        metal = "XAG"
    else:
        raise ValueError("metal must be XAU/gold or XAG/silver")

    interval = interval.lower()
    if interval not in ("daily", "monthly", "yearly"):
        raise ValueError("interval must be daily, monthly, or yearly")
    if not 1 <= limit <= 1000:
        raise ValueError("limit must be between 1 and 1000")

    params = {"metal": metal, "interval": interval, "limit": limit}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return api_get("history", params, CACHE_TTL_HISTORY)


if __name__ == "__main__":
    logger.info(
        "Starting Gold and Silver MCP on %s:%s (%s)",
        MCP_HOST,
        MCP_PORT,
        MCP_TRANSPORT,
    )
    mcp.run(transport=MCP_TRANSPORT, host=MCP_HOST, port=MCP_PORT)
