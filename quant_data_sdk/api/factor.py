"""
多因子接口
"""

from typing import Dict, Any, List


class FactorAPI:
    """多因子综合排名"""

    def __init__(self, client):
        self._client = client

    def get_ranking(
        self,
        top_n: int = 20,
        refresh: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        多因子综合排名

        打分公式：
          - 量比（15%）
          - 换手率（15%）
          - 涨跌幅（10%）
          - ROE（30%）
          - 净利率（20%）
          - 资产负债率（10%）

        :param top_n: 返回条数（1-500，默认 20）
        :return: 排名列表
        """
        return self._client.get("/factor/ranking", topN=top_n, refresh=refresh)