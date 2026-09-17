"""
异步客户端（基于 httpx）
"""

import asyncio
from typing import Optional

import httpx

from .exceptions import (
    QuantDataError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

DEFAULT_BASE_URL = "https://zizhenghua.com/api"
USER_AGENT = "quant-data-sdk-python/1.0.0"


class AsyncQuantDataClient:
    """
    异步 Quant Data API 客户端

    用法：
        import asyncio
        from quant_data_sdk import AsyncQuantDataClient

        async def main():
            async with AsyncQuantDataClient(api_key="your_key") as client:
                results = await asyncio.gather(
                    client.stock.get_realtime("600519"),
                    client.stock.get_realtime("000001"),
                )
                for r in results:
                    print(r["name"], r["latestPrice"])

        asyncio.run(main())
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        headers = {"User-Agent": USER_AGENT}
        if api_key:
            headers["X-API-Key"] = api_key

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

        from .api.async_stock import AsyncStockAPI
        from .api.async_market import AsyncMarketAPI
        from .api.async_sector import AsyncSectorAPI
        from .api.async_fin import AsyncFinAPI
        from .api.async_factor import AsyncFactorAPI
        from .api.async_ai import AsyncAIAPI

        self.stock = AsyncStockAPI(self)
        self.market = AsyncMarketAPI(self)
        self.sector = AsyncSectorAPI(self)
        self.fin = AsyncFinAPI(self)
        self.factor = AsyncFactorAPI(self)
        self.ai = AsyncAIAPI(self)

    async def _request(self, method: str, path: str, **kwargs):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = await self._client.request(method, path, **kwargs)

                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, dict) and "success" in data:
                        if not data["success"]:
                            raise QuantDataError(data.get("message", "Unknown"))
                        return data.get("data")
                    return data

                if resp.status_code == 401:
                    raise AuthenticationError(self._msg(resp, "API Key 无效"))
                if resp.status_code == 404:
                    raise NotFoundError(self._msg(resp, "资源不存在"))
                if resp.status_code == 429:
                    raise RateLimitError(
                        self._msg(resp, "请求过于频繁"),
                        is_anonymous=(self.api_key is None),
                    )
                if resp.status_code == 400:
                    raise ValidationError(self._msg(resp, "参数错误"))

                raise QuantDataError(self._msg(resp, f"HTTP {resp.status_code}"))

            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
                continue

        raise QuantDataError(
            f"请求失败（重试 {self.max_retries} 次）: {last_error}"
        )

    @staticmethod
    def _msg(resp, default: str) -> str:
        try:
            data = resp.json()
            if isinstance(data, dict) and "message" in data:
                return data["message"]
        except Exception:
            pass
        return default

    async def get(self, path: str, **params):
        """GET 请求"""
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: dict = None, **kwargs):
        """POST 请求"""
        if json is not None:
            return await self._request("POST", path, json=json)
        return await self._request("POST", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        """DELETE 请求"""
        return await self._request("DELETE", path, **kwargs)

    async def close(self):
        """关闭 httpx client"""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    def __repr__(self):
        auth = "API Key" if self.api_key else "匿名"
        return f"<AsyncQuantDataClient base_url={self.base_url} auth={auth}>"