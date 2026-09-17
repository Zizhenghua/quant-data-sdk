"""
QuantDataClient 单元测试

只测不依赖网络的部分（构造、参数校验、异常）。
真实 HTTP 请求用 tests/test_ai.py 或手动跑 examples/。
"""

import pytest

from quant_data_sdk import QuantDataClient
from quant_data_sdk.exceptions import (
    QuantDataError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)


class TestClientInit:
    """客户端初始化"""

    def test_default_base_url(self):
        client = QuantDataClient()
        assert client.base_url == "https://zizhenghua.com/api"
        client.close()

    def test_custom_base_url(self):
        client = QuantDataClient(base_url="http://127.0.0.1:8080/api")
        assert client.base_url == "http://127.0.0.1:8080/api"
        client.close()

    def test_base_url_trailing_slash(self):
        client = QuantDataClient(base_url="https://zizhenghua.com/api/")
        assert client.base_url == "https://zizhenghua.com/api"
        client.close()

    def test_with_api_key(self):
        client = QuantDataClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client._session.headers["X-API-Key"] == "test_key"
        client.close()

    def test_without_api_key(self):
        client = QuantDataClient()
        assert client.api_key is None
        assert "X-API-Key" not in client._session.headers
        client.close()

    def test_repr(self):
        client = QuantDataClient()
        assert "匿名" in repr(client)
        client.close()

        client2 = QuantDataClient(api_key="test_key")
        assert "API Key" in repr(client2)
        client2.close()

    def test_sub_apis_registered(self):
        client = QuantDataClient()
        assert client.stock is not None
        assert client.market is not None
        assert client.sector is not None
        assert client.fin is not None
        assert client.factor is not None
        assert client.ai is not None
        client.close()

    def test_context_manager(self):
        with QuantDataClient() as client:
            assert client is not None


class TestExceptions:
    """异常类"""

    def test_authentication_error_message(self):
        e = AuthenticationError("API Key 无效")
        assert "zizhenghua.com/profile" in str(e)
        assert "API Key 无效" in str(e)

    def test_rate_limit_error_anonymous(self):
        e = RateLimitError("请求过于频繁", is_anonymous=True)
        s = str(e)
        assert "匿名" in s
        assert "zizhenghua.com/register" in s

    def test_rate_limit_error_authenticated(self):
        e = RateLimitError("请求过于频繁", is_anonymous=False)
        s = str(e)
        assert "匿名" not in s

    def test_error_hierarchy(self):
        assert issubclass(AuthenticationError, QuantDataError)
        assert issubclass(RateLimitError, QuantDataError)
        assert issubclass(NotFoundError, QuantDataError)
        assert issubclass(ValidationError, QuantDataError)