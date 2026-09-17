"""
个股接口（异步）
"""

from typing import Dict, Any, List, Optional


class AsyncStockAPI:
    """个股行情、K线、PE/PB、选股（异步）"""

    def __init__(self, client):
        self._client = client

    async def get_realtime(self, code: str) -> Dict[str, Any]:
        return await self._client.get(f"/stock/realtime/{code}")

    async def get_kline(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        return await self._client.get(f"/stock/detail/{code}", **params)

    async def get_basic(self, code: str) -> Dict[str, Any]:
        return await self._client.get(f"/stock/basic/{code}")

    async def filter_stocks(self, **filters) -> List[Dict[str, Any]]:
        return await self._client.post("/stock/filter", json=filters)

    async def get_ranking(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/stock/ranking", refresh=refresh)

    async def get_losers(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/stock/losers", refresh=refresh)

    async def get_turnover_ranking(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/stock/turnover-ranking", refresh=refresh)