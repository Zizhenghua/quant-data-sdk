"""
Quant Data SDK
==============

官方 Python SDK for Quant Data API

用法：
    from quant_data_sdk import QuantDataClient

    # 匿名（30 次/天 AI，10 次/分钟数据）
    client = QuantDataClient()

    # 注册（100 次/天 AI，1000 次/天数据）
    client = QuantDataClient(api_key="your_key")

    # 数据接口
    data = client.stock.get_realtime("600519")

    # AI 接口
    result = client.ai.generate_bollinger("600519", "2023-01-01", "2025-12-31")
"""

from .client import QuantDataClient
from .exceptions import (
    QuantDataError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

__version__ = "1.0.0"
__author__ = "Zizhenghua"
__email__ = "support@zizhenghua.com"
__url__ = "https://github.com/Zizhenghua/quant-data-sdk"

__all__ = [
    "QuantDataClient",
    "QuantDataError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
]