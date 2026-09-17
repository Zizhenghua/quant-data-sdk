"""
行业接口
"""

from typing import Dict, Any, List


class SectorAPI:
    """申万行业指数"""

    def __init__(self, client):
        self._client = client

    def get_performance(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """
        行业涨跌幅（按涨跌幅降序）

        :return: [{"name": "银行", "changePercent": 2.5, "amount": 100000}, ...]
        """
        return self._client.get("/sector/performance", refresh=refresh)

    def get_amount_ranking(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """
        行业成交额排行

        :return: [{"name": "银行", "amount": 100000, "changePercent": 2.5}, ...]
        """
        return self._client.get("/sector/amount-ranking", refresh=refresh)

    def get_freshness(self) -> Dict[str, Any]:
        """行业数据最新日期"""
        return self._client.get("/sector/freshness")