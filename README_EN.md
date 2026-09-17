# Quant Data SDK

[![PyPI](https://img.shields.io/pypi/v/zizhenghua-quant.svg)](https://pypi.org/project/zizhenghua-quant/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Zizhenghua/quant-data-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Zizhenghua/quant-data-sdk/actions/workflows/test.yml)
[![Python](https://img.shields.io/pypi/pyversions/zizhenghua-quant.svg)](https://pypi.org/project/zizhenghua-quant/)
[![npm](https://img.shields.io/npm/v/zizhenghua-quant.svg)](https://www.npmjs.com/package/zizhenghua-quant)

[English](README_EN.md) | [中文](README.md)

Official Python & JavaScript SDK for [Quant Data API](https://zizhenghua.com).

A-share market data: quotes, financials, sectors, factors.

---

## ✨ Features

- 🚀 One-line A-share data access
- 🤖 AI code generation (natural language → strategy code)
- 🖥️ Built-in CLI (`quant-data`)
- 📊 pandas integration (`get_kline_df()`, etc.)
- ⚡ Async support (`AsyncQuantDataClient`)
- 📦 JavaScript/TypeScript SDK
- 🔐 Auto API Key authentication
- 🔁 Built-in retry, timeout, error handling
- 📝 Full type hints
- 📦 Context manager support (`with` syntax)
- 🆓 Anonymous access (no registration)

---

## 📦 Installation

### Python

```bash
# Basic
pip install zizhenghua-quant

# With pandas
pip install "zizhenghua-quant[pandas]"

# With async
pip install "zizhenghua-quant[async]"

# All
pip install "zizhenghua-quant[all]"
```

### JavaScript / TypeScript

```bash
npm install zizhenghua-quant
```

---

## 🚀 Quick Start

### 1. Get API Key (Optional)

Anonymous access works, but with lower limits.

1. Visit https://zizhenghua.com and register
2. Go to "Account Settings" → "API Key Management"
3. Click "+ Create New Key", save it (shown only once)

### 2. Python

```python
from quant_data_sdk import QuantDataClient

# Anonymous (30 AI calls/day, 10 data calls/min)
client = QuantDataClient()

# Or registered (100 AI calls/day, 1000 data calls/day)
client = QuantDataClient(api_key="your_api_key_here")

# Get realtime quote
data = client.stock.get_realtime("600519")
print(data)
```

### 3. JavaScript

```typescript
import { QuantDataClient } from 'zizhenghua-quant';

const client = new QuantDataClient({
  apiKey: 'your_api_key_here',  // optional
});

const data = await client.stock.getRealtime('600519');
console.log(data);
```

---

## 📖 Usage

### Data APIs

```python
from quant_data_sdk import QuantDataClient

client = QuantDataClient(api_key="your_key")

# Realtime quote
data = client.stock.get_realtime("600519")

# K-line
kline = client.stock.get_kline("600519", "2024-01-01", "2024-12-31")

# Stock screening
stocks = client.stock.filter_stocks(minTurnover=5, minRoe=15)

# Market stats
stats = client.market.get_stats()

# Sectors
sectors = client.sector.get_performance()

# Financials
fin = client.fin.get_latest("600519")

# Multi-factor ranking
ranking = client.factor.get_ranking(topN=20)
```

### pandas Integration

```python
# K-line → DataFrame
df = client.stock.get_kline_df("600519", "2024-01-01", "2024-12-31")
df["ma5"] = df["close"].rolling(5).mean()
df["ma20"] = df["close"].rolling(20).mean()
```

### Async

```python
import asyncio
from quant_data_sdk import AsyncQuantDataClient

async def main():
    async with AsyncQuantDataClient() as client:
        results = await asyncio.gather(
            client.stock.get_realtime("600519"),
            client.stock.get_realtime("601318"),
            client.stock.get_realtime("300750"),
        )
        for r in results:
            print(r["name"], r["latestPrice"])

asyncio.run(main())
```

### AI Code Generation

```python
result = client.ai.generate_code(
    prompt="Backtest Bollinger Bands for 600519 from 2023 to 2025",
    language="python"
)
code = client.ai.extract_code(result["raw"])
```

---

## 🖥️ CLI

```bash
# Realtime quote
quant-data stock realtime 600519

# K-line
quant-data stock kline 600519 --start 2024-01-01 --end 2024-12-31

# Export to CSV
quant-data stock kline 600519 --start 2024-01-01 -o kline.csv

# AI generate
quant-data ai generate "Write a dual MA strategy" -o backtest.py
```

---

## 📦 JavaScript/TypeScript SDK

```typescript
import { QuantDataClient } from 'zizhenghua-quant';

const client = new QuantDataClient({ apiKey: 'your_key' });

const data = await client.stock.getRealtime('600519');
const kline = await client.stock.getKline('600519', '2024-01-01', '2024-12-31');
const stats = await client.market.getStats();
```

---

## 📊 Rate Limits

| User | Data API | AI API |
|------|----------|--------|
| Anonymous | 10/min, 10,000 lines/min | 30/day |
| Registered | 300/min, 600,000 lines/min, 1000/day | 100/day |

Throws `RateLimitError` when exceeded.

---

## ❌ Error Handling

```python
from quant_data_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

try:
    data = client.stock.get_realtime("600519")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
```

---

## ❓ FAQ

### Can I use it anonymously?

Yes, but with lower limits:
- Data: 10/min, 10,000 lines/min
- AI: 30/day

Register for higher limits.

### How to get an API Key?

1. Visit https://zizhenghua.com
2. Register and log in
3. Go to "Account Settings" → "API Key Management"
4. Create a new key

### What stocks are supported?

All A-share stocks (SSE, SZSE, BSE), including indices and ETFs.

### Can I use it commercially?

SDK is MIT-licensed. Data API has free tiers.

### What Python versions are supported?

Python 3.8+.

### What Node versions are supported?

Node 16+.

### How to report issues?

https://github.com/Zizhenghua/quant-data-sdk/issues

---

---

## 💬 Discussions

Questions? Ask on [GitHub Discussions](https://github.com/Zizhenghua/quant-data-sdk/discussions).

---
## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Zizhenghua/quant-data-sdk&type=Date)](https://star-history.com/#Zizhenghua/quant-data-sdk&Date)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

[MIT](LICENSE)

---

## ⚠️ Disclaimer

Data is for quantitative research and backtesting only. Not investment advice.

AI-generated code is not guaranteed to be correct. Please review before use.