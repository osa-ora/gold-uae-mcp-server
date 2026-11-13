
# Gold & Silver MCP Server Demo

Simple Gold and Silver MCP Server that utilizes the public AlyawmGold API:

https://alyawmgold.com/developers

The server exposes gold and silver reference prices through MCP tools. The default market is the United Arab Emirates (AE).

## Available MCP Tools

- `get_today_gold_price` — Get the latest gold reference price.
- `get_today_silver_price` — Get the latest silver reference price.
- `get_today_metals_prices` — Get gold and silver prices together.
- `get_supported_markets` — List supported markets and currencies.
- `get_metal_price_history` — Retrieve historical gold (XAU) or silver (XAG) prices.

The current-price tools accept a two-letter market code. For example, use `AE` for the UAE.

Historical queries accept:
- `XAU` or `gold` for gold.
- `XAG` or `silver` for silver.

> **Note:** Prices are indicative market references, not jewellery-shop or dealer quotes. They exclude dealer spreads, premiums, making charges, taxes and other fees.

## Run Locally

Clone the Git repository and execute the following commands:

```bash
# Clone the repository
git clone https://github.com/osa-ora/gold-silver-mcp-server.git
cd gold-silver-mcp-server

# Create virtual environment
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python app.py
```

The server listens on port `8061` by default.

Configure your MCP client to connect to:

```text
http://127.0.0.1:8061/mcp
```

### Local Configuration

The server uses environment variables for configuration:

```bash
export MCP_HOST=0.0.0.0
export GOLD_SILVER_MCP_PORT=8061
export MCP_TRANSPORT=http
export GOLD_SILVER_API_BASE_URL=https://alyawmgold.com/api/v1
```

You can also use the provided `.env.example` as a reference.

No API key is required by the default configuration.

## Run over OpenShift

You can deploy the Gold & Silver MCP Server on OpenShift using the Python 3.12 UBI 10 S2I builder.

```bash
# Create a new OpenShift project
oc new-project gold-silver-mcp

# Create the Gold & Silver MCP server application using S2I
oc new-app python:3.12-minimal-ubi10~https://github.com/osa-ora/gold-silver-mcp-server --name=gold-silver-mcp-server -n gold-silver-mcp

# Apply the ConfigMap
oc apply -f config/configmap.yaml -n gold-silver-mcp

# Inject ConfigMap configuration into the deployment
oc set env deployment/gold-silver-mcp-server --from=configmap/gold-silver-mcp-config -n gold-silver-mcp

# Expose the service externally
oc expose svc/gold-silver-mcp-server -n gold-silver-mcp
```

### Verify the Deployment

```bash
# Check build and pod status
oc get builds,pods -n gold-silver-mcp

# Follow application logs
oc logs -f deployment/gold-silver-mcp-server -n gold-silver-mcp

# Get the external route
oc get route gold-silver-mcp-server -n gold-silver-mcp
```

### Connect to the Remote MCP Server

Once the OpenShift Route is ready, configure your remote MCP client using:

```text
https://<route-host>/mcp
```

For internal cluster access, use the service endpoint:

```text
http://gold-silver-mcp-server.gold-silver-mcp.svc:8080/mcp
```

The OpenShift ConfigMap configures the MCP server to listen on port `8080`.

## Configuration

The project includes:

- `.env.example` — Example environment configuration for local execution.
- `config/configmap.yaml` — OpenShift ConfigMap for remote deployment.

The main configuration options include:

| Variable | Default | Description |
|---|---|---|
| `MCP_HOST` | `0.0.0.0` | MCP server bind address |
| `GOLD_SILVER_MCP_PORT` | `8061` | MCP server port |
| `MCP_TRANSPORT` | `http` | MCP transport |
| `GOLD_SILVER_API_BASE_URL` | `https://alyawmgold.com/api/v1` | Upstream API endpoint |
| `GOLD_SILVER_API_TIMEOUT` | `15` | API request timeout |

## Project Structure

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

## Upstream API

AlyawmGold API documentation:

https://alyawmgold.com/developers
