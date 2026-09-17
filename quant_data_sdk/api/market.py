"""
市场接口
"""

from typing import Dict, Any, List


class MarketAPI:
    """市场统计、涨跌分布、异动榜"""

    def __init__(self, client):
        self._client = client

    def get_stats(self, refresh: bool = False) -> Dict[str, Any]:
        """
        市场统计：涨跌家数、涨跌停家数

        :return: {"total": 5000, "up": 2500, "down": 2400, "flat": 100, "limitUp": 45, "limitDown": 12}
        """
        return self._client.get("/market/stats", refresh=refresh)

    def get_stats_df(self, refresh: bool = False):
        """市场统计 → DataFrame"""
        from ..utils import to_dataframe
        return to_dataframe(self.get_stats(refresh))

    def get_histogram(self, refresh: bool = False) -> Dict[str, Any]:
        """
        涨跌幅分布直方图

        :return: {"bins": [{"range": "0%~1%", "count": 500}, ...], "total": 5000}
        """
        return self._client.get("/market/histogram", refresh=refresh)

    def get_histogram_df(self, refresh: bool = False):
        """涨跌幅分布 → DataFrame"""
        from ..utils import to_dataframe
        data = self.get_histogram(refresh)
        if isinstance(data, dict) and "bins" in data:
            return to_dataframe(data["bins"])
        return to_dataframe(data)

    def get_concentration(self, refresh: bool = False) -> Dict[str, Any]:
        """
        成交额集中度

        :return: {"concentration": 0.35}
        """
        return self._client.get("/market/concentration", refresh=refresh)

    def get_volume_spike(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """量比异动榜（量比 > 3，涨幅 2-8%）"""
        return self._client.get("/market/volume-spike", refresh=refresh)

    def get_volume_spike_df(self, refresh: bool = False):
        """量比异动榜 → DataFrame"""
        from ..utils import to_dataframe
        return to_dataframe(self.get_volume_spike(refresh))

    def get_amplitude_extreme(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """振幅极端榜（振幅 > 8%）"""
        return self._client.get("/market/amplitude-extreme", refresh=refresh)

    def get_amplitude_extreme_df(self, refresh: bool = False):
        """振幅极端榜 → DataFrame"""
        from ..utils import to_dataframe
        return to_dataframe(self.get_amplitude_extreme(refresh))

    def get_freshness(self) -> Dict[str, Any]:
        """
        数据新鲜度

        :return: {"lastUpdate": "2026-09-17 15:30:02", "totalCount": 5000, "lagMinutes": 5}
        """
        return self._client.get("/market/freshness")