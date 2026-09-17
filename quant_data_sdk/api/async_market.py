"""
市场接口（异步）
"""

from typing import Dict, Any, List


class AsyncMarketAPI:
    """市场统计、涨跌分布、异动榜（异步）"""

    def __init__(self, client):
        self._client = client

    async def get_stats(self, refresh: bool = False) -> Dict[str, Any]:
        return await self._client.get("/market/stats", refresh=refresh)

    async def get_histogram(self, refresh: bool = False) -> Dict[str, Any]:
        return await self._client.get("/market/histogram", refresh=refresh)

    async def get_concentration(self, refresh: bool = False) -> Dict[str, Any]:
        return await self._client.get("/market/concentration", refresh=refresh)

    async def get_volume_spike(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/market/volume-spike", refresh=refresh)

    async def get_amplitude_extreme(self, refresh: bool = False) -> List[Dict[str, Any]]:
        return await self._client.get("/market/amplitude-extreme", refresh=refresh)

    async def get_freshness(self) -> Dict[str, Any]:
        return await self._client.get("/market/freshness")