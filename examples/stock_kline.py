#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取个股 K 线

演示 K 线接口的用法。
"""

from quant_data_sdk import QuantDataClient


def main():
    client = QuantDataClient()

    # 获取茅台 2024 年 K 线
    code = "600519"
    kline = client.stock.get_kline(
        code,
        start_date="2024-01-01",
        end_date="2024-12-31",
    )

    print(f"股票 {code} 2024 年 K 线，共 {len(kline)} 条")
    print()

    # 打印前 5 条
    print("前 5 条：")
    for bar in kline[:5]:
        print(
            f"  {bar['date']}  "
            f"开 {bar['open']:.2f}  "
            f"收 {bar['close']:.2f}  "
            f"高 {bar['high']:.2f}  "
            f"低 {bar['low']:.2f}  "
            f"换手 {bar['turnover']:.2f}%"
        )

    # 统计
    if kline:
        first = kline[0]
        last = kline[-1]
        change = (last["close"] - first["open"]) / first["open"] * 100
        print(f"\n区间涨跌：{change:.2f}%")

    client.close()


if __name__ == "__main__":
    main()