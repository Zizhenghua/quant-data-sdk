#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速开始

演示 SDK 的基本用法。
"""

from quant_data_sdk import QuantDataClient


def main():
    # 1. 匿名（不传 api_key）
    print("=" * 60)
    print("1. 匿名调用")
    print("=" * 60)
    client = QuantDataClient()

    data = client.stock.get_realtime("600519")
    print(f"贵州茅台实时行情：")
    print(f"  最新价：{data.get('latestPrice')} 元")
    print(f"  涨跌幅：{data.get('changePercent')}%")
    print(f"  换手率：{data.get('turnover')}%")

    # 2. 市场统计
    print("\n" + "=" * 60)
    print("2. 市场统计")
    print("=" * 60)
    stats = client.market.get_stats()
    print(f"  总数：{stats.get('total')}")
    print(f"  上涨：{stats.get('up')}")
    print(f"  下跌：{stats.get('down')}")

    # 3. 带 API Key
    print("\n" + "=" * 60)
    print("3. 带 API Key（更高限额）")
    print("=" * 60)
    API_KEY = "your_api_key_here"
    if API_KEY != "your_api_key_here":
        client2 = QuantDataClient(api_key=API_KEY)
        sectors = client2.sector.get_performance()
        print(f"  行业数据：{len(sectors)} 条")
    else:
        print("  跳过（未配置 API_KEY）")

    client.close()
    print("\n✅ 完成")


if __name__ == "__main__":
    main()