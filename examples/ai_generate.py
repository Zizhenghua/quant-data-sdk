#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 生成策略代码

演示 AI 接口的用法。
"""

from quant_data_sdk import QuantDataClient


def main():
    # 匿名
    client = QuantDataClient()

    # 方式 1：通用方法
    print("=" * 60)
    print("1. 通用方法")
    print("=" * 60)

    result = client.ai.generate_code(
        prompt="我想查看茅台23年到25年的布林带回测情况",
        language="python",
    )

    print(f"剩余次数：{result['remaining']}")
    print(f"代码长度：{len(result['raw'])} 字符")

    # 提取纯代码
    code = client.ai.extract_code(result["raw"], "python")
    print(f"\n--- 代码前 30 行 ---")
    for line in code.split("\n")[:30]:
        print(line)

    # 保存到文件
    with open("bollinger_backtest.py", "w", encoding="utf-8") as f:
        f.write(code)
    print(f"\n✅ 已保存到 bollinger_backtest.py")

    # 方式 2：快捷方法
    print("\n" + "=" * 60)
    print("2. 快捷方法（双均线）")
    print("=" * 60)

    result2 = client.ai.generate_ma_cross(
        code="600519",
        start_date="2023-01-01",
        end_date="2025-12-31",
        fast=5,
        slow=20,
    )
    print(f"剩余次数：{result2['remaining']}")

    code2 = client.ai.extract_code(result2["raw"], "python")
    with open("ma_cross_backtest.py", "w", encoding="utf-8") as f:
        f.write(code2)
    print(f"✅ 已保存到 ma_cross_backtest.py")

    client.close()


if __name__ == "__main__":
    main()