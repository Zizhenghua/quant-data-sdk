"""
行业接口（异步）
"""

from typing import Dict, Any, List


class AsyncSectorAPI:
    """申万行业指数（异步）"""

    def __init__(self, client):
        self._client = client

    async def get_performance(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/sector/performance", refresh=refresh)

    async def get_amount_ranking(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/sector/amount-ranking", refresh=refresh)

    async def get_freshness(self) -> Dict[str, Any]:
        return await self._client.get("/sector/freshness")