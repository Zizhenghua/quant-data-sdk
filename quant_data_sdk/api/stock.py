"""
个股接口
"""

from typing import Dict, Any, List, Optional


class StockAPI:
    """个股行情、K线、PE/PB、选股"""

    def __init__(self, client):
        self._client = client

    # ============================================================
    # 实时行情
    # ============================================================

    def get_realtime(self, code: str) -> Dict[str, Any]:
        """
        获取个股实时行情

        :param code: 股票代码，如 "600519"
        :return: 实时行情字典
        """
        return self._client.get(f"/stock/realtime/{code}")

    # ============================================================
    # K 线
    # ============================================================

    def get_kline(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        获取个股 K 线

        :param code: 股票代码
        :param start_date: 起始日期 YYYY-MM-DD，默认最近 3 年
        :param end_date: 结束日期 YYYY-MM-DD，默认今天
        :return: K 线列表
        """
        params = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        return self._client.get(f"/stock/detail/{code}", **params)

    # ============================================================
    # PE/PB
    # ============================================================

    def get_basic(self, code: str) -> Dict[str, Any]:
        """
        获取个股 PE/PB

        :param code: 股票代码
        :return: 估值指标
        """
        return self._client.get(f"/stock/basic/{code}")

    # ============================================================
    # 选股
    # ============================================================

    def filter_stocks(self, **filters) -> List[Dict[str, Any]]:
        """
        多条件选股

        :param filters: 筛选条件
            - minTurnover: 换手率（%）
            - minVolumeRatio: 量比
            - minAmount: 成交额（元）
            - minChangePercent: 涨跌幅（%）
            - minAmplitude: 振幅（%）
            - minMarketCap: 总市值（万元）
            - minRoe: ROE（%）
            - minGrossMargin: 毛利率（%）
            - maxDebtToAssets: 资产负债率（%）
            - sortBy: 排序字段
            - sortOrder: asc / desc
            - limit: 返回条数（默认 100，最大 6000）
        :return: 符合条件的股票列表
        """
        return self._client.post("/stock/filter", json=filters)

    # ============================================================
    # 榜单
    # ============================================================

    def get_ranking(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """涨幅榜（前 20）"""
        return self._client.get("/stock/ranking", refresh=refresh)

    def get_losers(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """跌幅榜（前 20）"""
        return self._client.get("/stock/losers", refresh=refresh)

    def get_turnover_ranking(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """换手率榜（前 20）"""
        return self._client.get("/stock/turnover-ranking", refresh=refresh)