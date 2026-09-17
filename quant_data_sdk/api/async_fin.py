"""
财务接口（异步）
"""

from typing import Dict, Any, List


class AsyncFinAPI:
    """财务指标（异步）"""

    def __init__(self, client):
        self._client = client

    async def get_latest(self, code: str, refresh: bool = False) -> Dict[str, Any]:
        return await self._client.get(f"/fin/latest/{code}", refresh=refresh)

    async def get_history(
        self,
        code: str,
        n: int = 8,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        return await self._client.get(f"/fin/history/{code}", n=n, refresh=refresh)

    async def get_top_roe(
        self,
        limit: int = 20,
        min_roe: float = 0,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        return await self._client.get(
            "/fin/top/roe", limit=limit, minRoe=min_roe, refresh=refresh
        )