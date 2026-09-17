# Quant Data SDK

[![PyPI](https://img.shields.io/pypi/v/zizhenghua-quant.svg)](https://pypi.org/project/zizhenghua-quant/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Zizhenghua/quant-data-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Zizhenghua/quant-data-sdk/actions/workflows/test.yml)
[![Python](https://img.shields.io/pypi/pyversions/zizhenghua-quant.svg)](https://pypi.org/project/zizhenghua-quant/)
[![npm](https://img.shields.io/npm/v/zizhenghua-quant.svg)](https://www.npmjs.com/package/zizhenghua-quant)

[English](README_EN.md) | [中文](README.md)

Official Python & JavaScript SDK for [Quant Data API](https://zizhenghua.com).

A 股行情、财务、行业、因子数据的官方 Python / JavaScript SDK。

---

## ✨ Features

- 🚀 一行代码获取 A 股数据
- 🤖 AI 代码生成（自然语言 → 策略代码）
- 🖥️ 自带 CLI（`quant-data` 命令）
- 📊 pandas 集成（`get_kline_df()` 等）
- ⚡ 异步支持（`AsyncQuantDataClient`）
- 📦 JavaScript/TypeScript SDK
- 🔐 自动处理 API Key 认证
- 🔁 内置重试、超时、错误处理
- 📝 完整的类型提示（type hints）
- 📦 支持上下文管理器（`with` 语法）
- 🆓 支持匿名调用（无需注册）

---

## 📦 Installation

### Python

```bash
# 基础
pip install zizhenghua-quant

# 带 pandas（DataFrame 支持）
pip install "zizhenghua-quant[pandas]"

# 带异步（httpx）
pip install "zizhenghua-quant[async]"

# 全部
pip install "zizhenghua-quant[all]"
```

### JavaScript / TypeScript

```bash
npm install zizhenghua-quant
```

---

## 🚀 Quick Start

### 1. 获取 API Key（可选）

匿名也能用，但限额较低。注册后可获得更高限额。

1. 访问 https://zizhenghua.com 注册账号
2. 登录后进入「账号设置」→「API Key 管理」
3. 点击「+ 创建新 Key」，复制保存（只显示一次）

### 2. Python 调用

```python
from quant_data_sdk import QuantDataClient

# 匿名（30 次/天 AI，10 次/分钟数据）
client = QuantDataClient()

# 或注册（100 次/天 AI，1000 次/天数据）
client = QuantDataClient(api_key="your_api_key_here")

# 获取贵州茅台实时行情
data = client.stock.get_realtime("600519")
print(data)
```

### 3. JavaScript 调用

```typescript
import { QuantDataClient } from 'zizhenghua-quant';

const client = new QuantDataClient({
  apiKey: 'your_api_key_here',  // 可选
});

const data = await client.stock.getRealtime('600519');
console.log(data);
```

---

## 📖 使用示例

### 数据接口

```python
from quant_data_sdk import QuantDataClient

client = QuantDataClient(api_key="your_key")

# 实时行情
data = client.stock.get_realtime("600519")

# K 线
kline = client.stock.get_kline("600519", "2024-01-01", "2024-12-31")

# 多条件选股
stocks = client.stock.filter_stocks(minTurnover=5, minRoe=15)

# 市场统计
stats = client.market.get_stats()

# 行业数据
sectors = client.sector.get_performance()

# 财务指标
fin = client.fin.get_latest("600519")

# 多因子排名
ranking = client.factor.get_ranking(topN=20)
```

### pandas 集成

```python
# K 线 → DataFrame
df = client.stock.get_kline_df("600519", "2024-01-01", "2024-12-31")
df["ma5"] = df["close"].rolling(5).mean()
df["ma20"] = df["close"].rolling(20).mean()

# 涨幅榜 → DataFrame
df = client.stock.get_ranking_df()

# 行业 → DataFrame
df = client.sector.get_performance_df()
```

### 异步

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

### AI 代码生成

```python
# 通用方法
result = client.ai.generate_code(
    prompt="我想查看茅台23年到25年的布林带回测情况",
    language="python"
)
code = client.ai.extract_code(result["raw"])

# 快捷方法
client.ai.generate_bollinger("600519", "2023-01-01", "2025-12-31")
client.ai.generate_ma_cross("600519", "2023-01-01", "2025-12-31", fast=5, slow=20)
client.ai.generate_rsi("600519", "2023-01-01", "2025-12-31", oversold=30, overbought=70)
client.ai.generate_macd("600519", "2023-01-01", "2025-12-31")
client.ai.generate_kdj("600519", "2023-01-01", "2025-12-31")
```

### 上下文管理器

```python
with QuantDataClient(api_key="your_key") as client:
    data = client.stock.get_realtime("600519")
    print(data)
# 自动关闭
```

### 自定义 base URL

```python
# 本地开发
client = QuantDataClient(
    api_key="your_key",
    base_url="http://127.0.0.1:8080/api"
)
```

---

## 🖥️ CLI

安装后自带 `quant-data` 命令行工具。

### 数据查询

```bash
# 实时行情
quant-data stock realtime 600519

# 批量
quant-data stock realtime 600519 601318 001359

# K 线
quant-data stock kline 600519 --start 2024-01-01 --end 2024-12-31

# 涨幅榜
quant-data stock ranking

# 选股
quant-data stock filter --min-turnover 5 --min-roe 15 --limit 20

# 市场统计
quant-data market stats

# 行业涨跌幅
quant-data sector performance

# 财务指标
quant-data fin latest 600519

# 多因子排名
quant-data factor ranking --top 5
```

### 导出文件

```bash
# 导出 K 线为 CSV
quant-data stock kline 600519 --start 2024-01-01 --end 2024-12-31 -o kline.csv

# 导出涨幅榜为 JSON
quant-data stock ranking -o ranking.json

# `-o` 可以放任意位置
quant-data -o ranking.json stock ranking
```

### AI 生成

```bash
# 生成策略代码
quant-data ai generate "写一个双均线策略"

# 保存到文件
quant-data ai generate "写一个双均线策略" -o backtest.py

# Java 版本
quant-data ai generate "写一个双均线策略" --language java -o Backtest.java
```

### 用 API Key

```bash
quant-data --api-key your_key stock realtime 600519
```

---

## 📦 JavaScript/TypeScript SDK

除了 Python SDK，还提供 JS/TS SDK。

### 安装

```bash
npm install zizhenghua-quant
```

### 使用

```typescript
import { QuantDataClient } from 'zizhenghua-quant';

const client = new QuantDataClient({
  apiKey: 'your_api_key_here',  // 可选，不传则匿名
});

// 实时行情
const data = await client.stock.getRealtime('600519');

// K 线
const kline = await client.stock.getKline('600519', '2024-01-01', '2024-12-31');

// 涨幅榜
const ranking = await client.stock.getRanking();

// 市场统计
const stats = await client.market.getStats();

// 行业
const sectors = await client.sector.getPerformance();

// 财务
const fin = await client.fin.getLatest('600519');

// 多因子
const factors = await client.factor.getRanking(20);
```

### AI 代码生成

```typescript
const result = await client.ai.generateCode({
  prompt: '我想查看茅台23年到25年的布林带回测情况',
  language: 'python',
});

const code = AIAPI.extractCode(result.raw, 'python');
console.log(code);
```

---

## 📊 限流

| 用户 | 数据接口 | AI 接口 |
|------|---------|--------|
| 匿名 | 10 次/分钟，10,000 行/分钟 | 30 次/天 |
| 注册 | 300 次/分钟，600,000 行/分钟，1000 次/天 | 100 次/天 |

超限时抛 `RateLimitError`，并提示注册。

---

## ❌ 错误处理

```python
from quant_data_sdk import QuantDataClient
from quant_data_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

client = QuantDataClient(api_key="your_key")

try:
    data = client.stock.get_realtime("600519")
except AuthenticationError as e:
    print(f"认证失败: {e}")
except RateLimitError as e:
    print(f"限流: {e}")
except NotFoundError as e:
    print(f"资源不存在: {e}")
except ValidationError as e:
    print(f"参数错误: {e}")
```

---

## 📚 Documentation

- [快速开始](examples/quickstart.py)
- [K 线](examples/stock_kline.py)
- [选股](examples/filter_stocks.py)
- [AI 生成](examples/ai_generate.py)
- [API 文档](https://zizhenghua.com/swagger-ui/index.html)

---

## ❓ FAQ

### 1. 匿名能用吗？

能，但限额较低：
- 数据接口：10 次/分钟，10,000 行/分钟
- AI 接口：30 次/天

注册后可获得更高限额。

### 2. 怎么拿 API Key？

1. 访问 https://zizhenghua.com 注册
2. 登录后进入「账号设置」→「API Key 管理」
3. 点击「+ 创建新 Key」，复制保存

### 3. 支持哪些股票？

A 股全市场（沪深京），包括指数、ETF。

### 4. 数据从哪来？

公开数据源，仅供学习研究。

### 5. 能商用吗？

SDK 是 MIT 协议，可以商用。数据接口有免费额度。

### 6. 报错 `RateLimitError` 怎么办？

- 等 1 分钟
- 或注册获取更高限额
- 或加 API Key

### 7. Python 和 JS SDK 有什么区别？

功能基本一致，语言不同：
- Python：支持 pandas / 异步 / CLI
- JS/TS：支持 TypeScript 类型

### 8. 支持哪些 Python 版本？

Python 3.8+。

### 9. 支持哪些 Node 版本？

Node 16+。

### 10. 怎么提 issue？

https://github.com/Zizhenghua/quant-data-sdk/issues

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

数据仅供量化学习与策略回测研究之用，不构成任何投资建议。

AI 生成的代码不保证正确性，请自行检查后再使用。