# Quant Data SDK

[![PyPI](https://img.shields.io/pypi/v/zizhenghua-quant.svg)](https://pypi.org/project/zizhenghua-quant/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Zizhenghua/quant-data-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Zizhenghua/quant-data-sdk/actions/workflows/test.yml)
[![Python](https://img.shields.io/pypi/pyversions/zizhenghua-quant.svg)](https://pypi.org/project/zizhenghua-quant/)

Official Python SDK for [Quant Data API](https://zizhenghua.com).

A 股行情、财务、行业、因子数据的官方 Python SDK。

---

## ✨ Features

- 🚀 一行代码获取 A 股数据
- 🤖 AI 代码生成（自然语言 → 策略代码）
- 🔐 自动处理 API Key 认证
- 🔁 内置重试、超时、错误处理
- 📝 完整的类型提示（type hints）
- 📦 支持上下文管理器（`with` 语法）
- 🆓 支持匿名调用（无需注册）

---

## 📦 Installation

```bash
pip install zizhenghua-quant
```

---

## 🚀 Quick Start

### 1. 获取 API Key（可选）

匿名也能用，但限额较低。注册后可获得更高限额。

1. 访问 https://zizhenghua.com 注册账号
2. 登录后进入「账号设置」→「API Key 管理」
3. 点击「+ 创建新 Key」，复制保存（只显示一次）

### 2. 调用

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

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

[MIT](LICENSE)

---

## ⚠️ Disclaimer

数据仅供量化学习与策略回测研究之用，不构成任何投资建议。

AI 生成的代码不保证正确性，请自行检查后再使用。