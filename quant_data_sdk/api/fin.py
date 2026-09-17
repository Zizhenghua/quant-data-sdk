"""
财务接口
"""

from typing import Dict, Any, List


class FinAPI:
    """财务指标"""

    def __init__(self, client):
        self._client = client

    def get_latest(self, code: str, refresh: bool = False) -> Dict[str, Any]:
        """
        最新一期财务指标

        :param code: 股票代码
        :return: 财务指标字典
        """
        return self._client.get(f"/fin/latest/{code}", refresh=refresh)

    def get_history(
        self,
        code: str,
        n: int = 8,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        财务历史（最近 N 期）

        :param code: 股票代码
        :param n: 期数（默认 8，最大 6000）
        """
        return self._client.get(f"/fin/history/{code}", n=n, refresh=refresh)

    def get_top_roe(
        self,
        limit: int = 20,
        min_roe: float = 0,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        ROE 排名

        :param limit: 返回条数（默认 20，最大 6000）
        :param min_roe: 最小 ROE（%）
        """
        return self._client.get(
            "/fin/top/roe", limit=limit, minRoe=min_roe, refresh=refresh
        )