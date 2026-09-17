"""
QuantDataClient 主入口
"""

import time
from typing import Optional

import requests

from .exceptions import (
    QuantDataError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


DEFAULT_BASE_URL = "https://zizhenghua.com/api"
USER_AGENT = "quant-data-sdk-python/1.0.0"


class QuantDataClient:
    """
    Quant Data API 客户端

    用法：
        # 匿名
        client = QuantDataClient()

        # 注册
        client = QuantDataClient(api_key="your_key")

        # 自定义 base URL（本地开发）
        client = QuantDataClient(api_key="your_key", base_url="http://127.0.0.1:8080/api")

        # 上下文管理器
        with QuantDataClient(api_key="your_key") as client:
            data = client.stock.get_realtime("600519")

    参数：
        api_key: API Key（可选，不传则匿名）
        base_url: API 基础地址，默认 https://zizhenghua.com/api
        timeout: 请求超时（秒），默认 30
        max_retries: 最大重试次数，默认 3
        verbose: 是否打印调试信息，默认 False
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
        max_retries: int = 3,
        verbose: bool = False,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.verbose = verbose

        self._session = requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        if api_key:
            self._session.headers["X-API-Key"] = api_key

        # 延迟导入，避免循环依赖
        from .api.stock import StockAPI
        from .api.market import MarketAPI
        from .api.sector import SectorAPI
        from .api.fin import FinAPI
        from .api.factor import FactorAPI
        from .api.ai import AIAPI

        self.stock = StockAPI(self)
        self.market = MarketAPI(self)
        self.sector = SectorAPI(self)
        self.fin = FinAPI(self)
        self.factor = FactorAPI(self)
        self.ai = AIAPI(self)

    # ============================================================
    # 内部请求方法
    # ============================================================

    def _request(self, method: str, path: str, **kwargs):
        """
        统一请求封装：
          - URL 拼接
          - 超时
          - 重试（指数退避）
          - 错误解析
        """
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                if self.verbose:
                    print(f"[QuantData] {method} {url} (attempt {attempt + 1})")
                    if "json" in kwargs:
                        print(f"[QuantData] body={kwargs['json']}")

                resp = self._session.request(method, url, **kwargs)

                # ===== 200 =====
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                    except ValueError:
                        return resp.text

                    # 统一格式 {success, message, data}
                    if isinstance(data, dict) and "success" in data:
                        if not data["success"]:
                            raise QuantDataError(data.get("message", "Unknown error"))
                        return data.get("data")
                    return data

                # ===== 401 =====
                if resp.status_code == 401:
                    msg = self._extract_message(resp, "API Key 无效")
                    raise AuthenticationError(msg)

                # ===== 404 =====
                if resp.status_code == 404:
                    msg = self._extract_message(resp, "资源不存在")
                    raise NotFoundError(msg)

                # ===== 429 =====
                if resp.status_code == 429:
                    msg = self._extract_message(resp, "请求过于频繁")
                    raise RateLimitError(msg, is_anonymous=(self.api_key is None))

                # ===== 400 =====
                if resp.status_code == 400:
                    msg = self._extract_message(resp, "参数错误")
                    raise ValidationError(msg)

                # ===== 其他 =====
                msg = self._extract_message(resp, f"HTTP {resp.status_code}")
                raise QuantDataError(msg)

            except (requests.ConnectionError, requests.Timeout) as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait = 2 ** attempt
                    if self.verbose:
                        print(f"[QuantData] 请求失败，{wait}s 后重试: {e}")
                    time.sleep(wait)
                continue

        raise QuantDataError(f"请求失败（重试 {self.max_retries} 次）: {last_error}")

    @staticmethod
    def _extract_message(resp, default: str) -> str:
        """从响应里提取 message"""
        try:
            data = resp.json()
            if isinstance(data, dict) and "message" in data:
                return data["message"]
        except ValueError:
            pass
        return default

    # ============================================================
    # 公开方法
    # ============================================================

    def get(self, path: str, **params):
        """GET 请求"""
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict = None, **kwargs):
        """
        POST 请求

        :param path: API 路径
        :param json: 请求体（dict），会作为 JSON body 发送
        :param kwargs: 其他参数，透传给 requests
        """
        if json is not None:
            return self._request("POST", path, json=json)
        return self._request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs):
        """DELETE 请求"""
        return self._request("DELETE", path, **kwargs)

    def health(self):
        """检查 API 是否可用"""
        return self.get("/market/stats")

    def close(self):
        """关闭 session"""
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        auth = "API Key" if self.api_key else "匿名"
        return f"<QuantDataClient base_url={self.base_url} auth={auth}>"