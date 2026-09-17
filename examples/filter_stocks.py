#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多条件选股

演示选股接口的用法。
"""

from quant_data_sdk import QuantDataClient


def main():
    client = QuantDataClient()

    # 筛选：换手率 > 5%，ROE > 15%
    print("选股条件：换手率 > 5%，ROE > 15%")
    print()

    stocks = client.stock.filter_stocks(
        minTurnover=5,
        minRoe=15,
        sortBy="turnover",
        sortOrder="desc",
        limit=20,
    )

    print(f"共 {len(stocks)} 只股票满足条件：")
    print()
    print(f"{'代码':<8} {'名称':<12} {'最新价':>8} {'涨跌幅':>8} {'换手率':>8}")
    print("-" * 60)

    for s in stocks:
        print(
            f"{s['code']:<8} "
            f"{s['name']:<12} "
            f"{s['latestPrice']:>8.2f} "
            f"{s['changePercent']:>7.2f}% "
            f"{s['turnover']:>7.2f}%"
        )

    client.close()


if __name__ == "__main__":
    main()