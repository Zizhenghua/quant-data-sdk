"""
Quant Data SDK
==============

官方 Python SDK for Quant Data API
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


def __getattr__(name):
    """延迟加载 AsyncQuantDataClient（需要 httpx）"""
    if name == "AsyncQuantDataClient":
        try:
            from .async_client import AsyncQuantDataClient
            return AsyncQuantDataClient
        except ImportError:
            raise ImportError(
                "需要 httpx 才能使用异步客户端。\n"
                "安装：pip install zizhenghua-quant[async]"
            )
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")