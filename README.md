# 🌐 Universal On-Chain Balance Tracker

<div align="center">

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

**A powerful, multi-chain wallet balance tracker supporting EVM and Solana networks**

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [CLI Usage](#-cli-usage) • [Docker](#-docker-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Supported Networks](#-supported-networks)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [CLI Usage](#-cli-usage)
- [API Documentation](#-api-documentation)
- [Docker Deployment](#-docker-deployment)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🎯 Overview

**Universal On-Chain Balance Tracker** is a comprehensive tool for tracking cryptocurrency wallet balances across multiple blockchain networks. It supports both EVM-compatible chains (Ethereum, Polygon, Arbitrum, etc.) and Solana, providing a unified interface for balance queries.

Perfect for:
- Crypto analysts and traders
- Portfolio managers
- DeFi developers
- Blockchain researchers
- Anyone needing multi-chain balance tracking

---

## ✨ Features

- **Multi-Chain Support**: Track balances across 7+ blockchain networks
- **EVM Compatible**: Ethereum, Arbitrum, Optimism, Base, BNB Chain, Polygon
- **Solana Support**: Native SOL and SPL token balances
- **Token Tracking**: Automatically checks popular tokens (USDC, USDT, WETH, etc.)
- **Dual Interface**: Both CLI and REST API available
- **Address Validation**: Automatic detection and validation of address types
- **Docker Ready**: Easy deployment with Docker and Docker Compose
- **Fast & Efficient**: Optimized RPC calls with connection pooling
- **Well Documented**: Interactive API docs with Swagger UI
- **Free to Use**: Works with public RPC endpoints (premium providers supported)

---

## 🌍 Supported Networks

| Network | Type | Native Token | Chain ID | Status |
|---------|------|--------------|----------|--------|
| Ethereum | EVM | ETH | 1 | ✅ |
| Arbitrum One | EVM | ETH | 42161 | ✅ |
| Optimism | EVM | ETH | 10 | ✅ |
| Base | EVM | ETH | 8453 | ✅ |
| BNB Smart Chain | EVM | BNB | 56 | ✅ |
| Polygon | EVM | MATIC | 137 | ✅ |
| Solana | Solana | SOL | - | ✅ |

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/Universal-On-Chain-Balance-Tracker.git
cd Universal-On-Chain-Balance-Tracker

# Start the API server
docker-compose up -d

# Access API documentation at http://localhost:8000
```

### Using Python

```bash
# Install dependencies
pip install -r requirements.txt

# Check balance via CLI
python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

# Start API server
python api.py
```

---

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Universal-On-Chain-Balance-Tracker.git
   cd Universal-On-Chain-Balance-Tracker
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure RPC endpoints (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred RPC endpoints
   ```

---

## 💻 CLI Usage

The CLI provides a simple interface for checking wallet balances from the command line.

### Basic Usage

```bash
# Check EVM address
python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

# Check Solana address
python main.py --address 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM
```

### Output Formats

```bash
# Text output (default, human-readable)
python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --format text

# JSON output (machine-readable)
python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --format json
```

### Filter Networks

```bash
# Check only specific networks
python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --networks ethereum polygon

# Check only Arbitrum and Optimism
python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --networks arbitrum optimism
```

### CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--address` | `-a` | Wallet address (required) | - |
| `--format` | `-f` | Output format (json/text) | text |
| `--networks` | `-n` | Specific networks to check | all |

### Example Output

```
================================================================================
BALANCE TRACKER RESULTS FOR: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
================================================================================

Ethereum (ETH)
----------------------------------------
Native Balance: 1.234567 ETH

Tokens (3):
  • USDC: 1000.50
  • USDT: 500.25
  • WETH: 0.5

Explorer: https://etherscan.io/address/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

Polygon (MATIC)
----------------------------------------
Native Balance: 50.123456 MATIC

Tokens (1):
  • USDC: 250.75

Explorer: https://polygonscan.com/address/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

================================================================================
Total Networks Checked: 7
================================================================================
```

---

## 🌐 API Documentation

The API provides RESTful endpoints for programmatic access to balance data.

### Starting the API Server

```bash
# Start with default settings (localhost:8000)
python api.py

# Custom host and port
python api.py --host 0.0.0.0 --port 8080

# Development mode with auto-reload
python api.py --reload
```

### API Endpoints

#### `GET /balances`

Get wallet balances across all or specific networks.

**Parameters:**
- `address` (required): Wallet address
- `networks` (optional): Comma-separated list of networks

**Example Requests:**

```bash
# Get all balances for an EVM address
curl "http://localhost:8000/balances?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# Get balances for specific networks
curl "http://localhost:8000/balances?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&networks=ethereum,polygon"

# Get Solana balances
curl "http://localhost:8000/balances?address=9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
```

**Example Response:**

```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "networks": [
    {
      "network": "Ethereum",
      "chain_id": 1,
      "native_token": "ETH",
      "native_balance": "1234567890000000000",
      "native_balance_formatted": "1.234567",
      "tokens": [
        {
          "symbol": "USDC",
          "name": "USD Coin",
          "balance": "1000500000",
          "balance_formatted": "1000.5",
          "decimals": 6,
          "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        }
      ],
      "explorer_url": "https://etherscan.io/address/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    }
  ],
  "total_networks_checked": 7,
  "success": true
}
```

#### `GET /validate`

Validate an address and detect its type.

**Parameters:**
- `address` (required): Address to validate

**Example Request:**

```bash
curl "http://localhost:8000/validate?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
```

**Example Response:**

```json
{
  "valid": true,
  "type": "evm",
  "checksum_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "message": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
}
```

#### `GET /networks`

Get list of supported networks.

**Example Request:**

```bash
curl "http://localhost:8000/networks"
```

**Example Response:**

```json
{
  "total_networks": 7,
  "networks": [
    {
      "key": "ethereum",
      "name": "Ethereum",
      "chain_id": 1,
      "native_token": "ETH",
      "type": "EVM"
    },
    ...
  ]
}
```

#### `GET /health`

Health check endpoint.

**Example Request:**

```bash
curl "http://localhost:8000/health"
```

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Start the service**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the service**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image**
   ```bash
   docker build -t balance-tracker .
   ```

2. **Run API server**
   ```bash
   docker run -p 8000:8000 balance-tracker
   ```

3. **Run CLI**
   ```bash
   docker run balance-tracker python main.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
   ```

### Development Mode

Run with auto-reload for development:

```bash
docker-compose --profile dev up
```

This starts the service on port 8001 with volume mounting for live code updates.

---

## ⚙️ Configuration

### RPC Endpoints

The application uses public RPC endpoints by default. For production use, configure your own RPC endpoints in `.env`:

```bash
# Copy example config
cp .env.example .env

# Edit with your RPC endpoints
nano .env
```

### Recommended RPC Providers

**For EVM Chains:**
- [Infura](https://infura.io) - Free tier available
- [Alchemy](https://alchemy.com) - Free tier available
- [QuickNode](https://quicknode.com) - Premium service

**For Solana:**
- [Helius](https://helius.dev) - Specialized Solana RPC
- [QuickNode](https://quicknode.com) - Multi-chain support
- [Alchemy](https://alchemy.com) - Solana support

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ETHEREUM_RPC` | Ethereum RPC endpoint | https://eth.llamarpc.com |
| `ARBITRUM_RPC` | Arbitrum RPC endpoint | https://arb1.arbitrum.io/rpc |
| `OPTIMISM_RPC` | Optimism RPC endpoint | https://mainnet.optimism.io |
| `BASE_RPC` | Base RPC endpoint | https://mainnet.base.org |
| `BNB_RPC` | BNB Chain RPC endpoint | https://bsc-dataseed.binance.org |
| `POLYGON_RPC` | Polygon RPC endpoint | https://polygon-rpc.com |
| `SOLANA_RPC` | Solana RPC endpoint | https://api.mainnet-beta.solana.com |

---

## 📚 Examples

### Python Integration

```python
from app.chains.evm import get_all_evm_balances
from app.chains.solana import get_solana_balances

# Get EVM balances
address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
balances = get_all_evm_balances(address)

for network in balances:
    print(f"{network.network}: {network.native_balance_formatted} {network.native_token}")
    for token in network.tokens:
        print(f"  {token.symbol}: {token.balance_formatted}")

# Get Solana balance
sol_address = "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
sol_balance = get_solana_balances(sol_address)
print(f"SOL: {sol_balance.native_balance_formatted}")
```

### JavaScript/TypeScript Integration

```javascript
// Fetch balances from API
async function getBalances(address) {
  const response = await fetch(
    `http://localhost:8000/balances?address=${address}`
  );
  const data = await response.json();
  return data;
}

// Usage
const address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb";
const balances = await getBalances(address);
console.log(balances);
```

### cURL Examples

```bash
# Get all balances
curl "http://localhost:8000/balances?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# Get specific networks
curl "http://localhost:8000/balances?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb&networks=ethereum,arbitrum"

# Validate address
curl "http://localhost:8000/validate?address=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# Get supported networks
curl "http://localhost:8000/networks"
```

---

## 🛠 Development

### Project Structure

```
Universal-On-Chain-Balance-Tracker/
├── app/
│   ├── __init__.py
│   ├── config.py           # Network configurations
│   ├── models.py           # Pydantic models
│   ├── validators.py       # Address validation
│   ├── chains/
│   │   ├── __init__.py
│   │   ├── evm.py         # EVM blockchain client
│   │   └── solana.py      # Solana blockchain client
│   └── tokens/
│       ├── __init__.py
│       └── tokens_config.py # Popular tokens list
├── main.py                 # CLI interface
├── api.py                  # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env.example          # Environment variables template
└── README.md             # This file
```

### Adding New Networks

1. **For EVM networks**, add to `app/config.py`:
   ```python
   "network_name": {
       "name": "Network Name",
       "chain_id": 123,
       "rpc_url": os.getenv("NETWORK_RPC", "https://rpc.network.com"),
       "native_token": "TOKEN",
       "decimals": 18,
       "explorer": "https://explorer.network.com"
   }
   ```

2. **Add popular tokens** in `app/tokens/tokens_config.py`

3. **Add environment variable** in `.env.example`

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests (when available)
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Connection timeout" errors
- **Solution**: Check your RPC endpoints, consider using premium providers

**Issue**: "Rate limit exceeded"
- **Solution**: Use your own RPC API keys instead of public endpoints

**Issue**: "Invalid address" error
- **Solution**: Ensure address format is correct (0x... for EVM, base58 for Solana)

**Issue**: Slow response times
- **Solution**: Configure faster RPC endpoints or use caching

### Getting Help

- Check the [Issues](https://github.com/yourusername/Universal-On-Chain-Balance-Tracker/issues) page
- Read the [API documentation](http://localhost:8000/) when server is running
- Review logs: `docker-compose logs` or check console output

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Update README.md for new features
- Test your changes thoroughly

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Blockchain interactions via [web3.py](https://web3py.readthedocs.io/) and [solana-py](https://michaelhly.com/solana-py/)
- Inspired by the need for unified multi-chain balance tracking

---

## 📊 Status

- ✅ **Production Ready**: Stable and actively maintained
- ✅ **Docker Support**: Containerized deployment available
- ✅ **API Documentation**: Interactive Swagger UI included
- ✅ **Multi-Chain**: EVM + Solana support
- 🔄 **Active Development**: Regular updates and improvements

---

<div align="center">

**Made with ❤️ for the crypto community**

[Report Bug](https://github.com/yourusername/Universal-On-Chain-Balance-Tracker/issues) • [Request Feature](https://github.com/yourusername/Universal-On-Chain-Balance-Tracker/issues)

</div>
