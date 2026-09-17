"""
多因子接口（异步）
"""

from typing import Dict, Any, List


class AsyncFactorAPI:
    """多因子综合排名（异步）"""

    def __init__(self, client):
        self._client = client

    async def get_ranking(
        self,
        top_n: int = 20,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        return await self._client.get("/factor/ranking", topN=top_n, refresh=refresh)