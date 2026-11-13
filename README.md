# Gold & Silver MCP Server

A lightweight Python MCP server exposing gold and silver reference prices through the public AlyawmGold API.

## MCP tools

- `get_today_gold_price(country="AE")` — latest gold reference price.
- `get_today_silver_price(country="AE")` — latest silver reference price.
- `get_today_metals_prices(country="AE")` — gold and silver together.
- `get_supported_markets()` — supported markets and currencies.
- `get_metal_price_history(metal="XAU", interval="daily", limit=30)` — historical gold or silver prices.

The default market is AE (United Arab Emirates).

> Prices are indicative reference prices, not dealer or jewellery-shop quotes. They exclude dealer spreads, premiums, making charges, taxes and fees. Verify endpoint availability and response fields against the provider's current API documentation before production use.

## Requirements

- Python 3.10+
- Outbound HTTPS access to `alyawmgold.com`
- No API key is configured by this server

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Default MCP Streamable HTTP endpoint: `http://127.0.0.1:8061/mcp`.

## Configuration

See `.env.example`. The default upstream API base URL is `https://alyawmgold.com/api/v1`.

## OpenShift

Apply the ConfigMap:

```bash
oc apply -f config/configmap.yaml
```

Reference it in your Deployment:

```yaml
envFrom:
  - configMapRef:
      name: gold-silver-mcp-config
```

Configure the container port as `8080`. Build and deploy using your normal Python/OpenShift build process.

## Project layout

```text
gold-silver-mcp-server/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
└── config/
    └── configmap.yaml
```

API documentation: https://alyawmgold.com/developers
