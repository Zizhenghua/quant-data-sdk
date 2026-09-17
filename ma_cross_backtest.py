# -*- coding: utf-8 -*-
"""
贵州茅台(600519) 5日均线 / 20日均线 金叉死叉策略回测
数据源: akshare (免费)
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ============ 1. 参数设置 ============
STOCK_CODE = "600519"
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
SHORT_WINDOW = 5      # 短均线
LONG_WINDOW = 20      # 长均线
INIT_CASH = 100000.0  # 初始资金
COMMISSION = 0.0003   # 单边手续费 万三
STAMP_TAX = 0.001     # 印花税(卖出) 千一

# ============ 2. 数据获取 ============
print("正在获取数据...")
df = ak.stock_zh_a_hist(
    symbol=STOCK_CODE,
    period="daily",
    start_date=START_DATE.replace("-", ""),
    end_date=END_DATE.replace("-", ""),
    adjust="qfq"  # 前复权
)

# 统一列名
df = df.rename(columns={
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume"
})
df["date"] = pd.to_datetime(df["date"])
df = df[["date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
df = df.sort_values("date").reset_index(drop=True)

print(f"共获取 {len(df)} 条日线数据，区间: {df['date'].iloc[0].date()} ~ {df['date'].iloc[-1].date()}")

# ============ 3. 计算均线 & 信号 ============
df["ma_short"] = df["close"].rolling(SHORT_WINDOW).mean()
df["ma_long"] = df["close"].rolling(LONG_WINDOW).mean()

# 金叉: 短均线上穿长均线; 死叉: 短均线下穿长均线
df["signal"] = 0
df.loc[(df["ma_short"] > df["ma_long"]) &
       (df["ma_short"].shift(1) <= df["ma_long"].shift(1)), "signal"] = 1   # 买入
df.loc[(df["ma_short"] < df["ma_long"]) &
       (df["ma_short"].shift(1) >= df["ma_long"].shift(1)), "signal"] = -1  # 卖出

# ============ 4. 回测执行(逐日循环) ============
cash = INIT_CASH
shares = 0
position = 0  # 0 空仓, 1 持仓

trade_records = []   # 每笔交易记录
equity_curve = []    # 每日总资产

for i in range(len(df)):
    row = df.iloc[i]
    price = row["close"]
    sig = row["signal"]

    # 买入信号 & 空仓
    if sig == 1 and position == 0:
        # 用全部资金买入(按100股取整)
        max_shares = int(cash / (price * (1 + COMMISSION)) // 100) * 100
        if max_shares > 0:
            cost = max_shares * price
            fee = cost * COMMISSION
            cash -= (cost + fee)
            shares = max_shares
            position = 1
            trade_records.append({
                "date": row["date"], "type": "buy",
                "price": price, "shares": shares, "fee": fee
            })

    # 卖出信号 & 持仓
    elif sig == -1 and position == 1:
        revenue = shares * price
        fee = revenue * COMMISSION + revenue * STAMP_TAX
        cash += (revenue - fee)
        trade_records.append({
            "date": row["date"], "type": "sell",
            "price": price, "shares": shares, "fee": fee
        })
        shares = 0
        position = 0

    # 记录每日总资产
    total = cash + shares * price
    equity_curve.append(total)

df["equity"] = equity_curve

# 若最后一天仍持仓, 按收盘价平仓(仅用于统计)
if position == 1:
    last_price = df["close"].iloc[-1]
    revenue = shares * last_price
    fee = revenue * COMMISSION + revenue * STAMP_TAX
    cash += (revenue - fee)
    trade_records.append({
        "date": df["date"].iloc[-1], "type": "sell",
        "price": last_price, "shares": shares, "fee": fee
    })
    shares = 0
    position = 0

# ============ 5. 收益统计 ============
final_equity = cash
total_return = (final_equity - INIT_CASH) / INIT_CASH * 100

# 最大回撤
equity_series = df["equity"]
running_max = equity_series.cummax()
drawdown = (equity_series - running_max) / running_max
max_drawdown = drawdown.min() * 100

# 交易配对统计
trades = []
buy_info = None
for rec in trade_records:
    if rec["type"] == "buy":
        buy_info = rec
    elif rec["type"] == "sell" and buy_info is not None:
        profit = (rec["price"] - buy_info["price"]) * rec["shares"] - rec["fee"] - buy_info["fee"]
        trades.append({
            "buy_date": buy_info["date"],
            "sell_date": rec["date"],
            "buy_price": buy_info["price"],
            "sell_price": rec["price"],
            "shares": rec["shares"],
            "profit": profit
        })
        buy_info = None

trade_count = len(trades)
win_count = sum(1 for t in trades if t["profit"] > 0)
win_rate = (win_count / trade_count * 100) if trade_count > 0 else 0.0

# 年化收益
days = (df["date"].iloc[-1] - df["date"].iloc[0]).days
annual_return = ((final_equity / INIT_CASH) ** (365 / days) - 1) * 100 if days > 0 else 0

# 基准: 买入并持有
benchmark_return = (df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0] * 100

print("\n" + "=" * 50)
print(f"股票代码: {STOCK_CODE}")
print(f"回测区间: {START_DATE} ~ {END_DATE}")
print(f"策略: {SHORT_WINDOW}日均线 / {LONG_WINDOW}日均线 金叉死叉")
print("=" * 50)
print(f"初始资金:      {INIT_CASH:,.2f} 元")
print(f"期末资产:      {final_equity:,.2f} 元")
print(f"总收益率:      {total_return:.2f}%")
print(f"年化收益率:    {annual_return:.2f}%")
print(f"最大回撤:      {max_drawdown:.2f}%")
print(f"交易次数:      {trade_count} 次")
print(f"盈利次数:      {win_count} 次")
print(f"胜率:          {win_rate:.2f}%")
print(f"买入持有收益:  {benchmark_return:.2f}%")
print("=" * 50)

if trade_count > 0:
    print("\n交易明细:")
    for i, t in enumerate(trades, 1):
        print(f"  #{i} 买 {t['buy_date'].date()} @ {t['buy_price']:.2f} "
              f"-> 卖 {t['sell_date'].date()} @ {t['sell_price']:.2f} "
              f"| 盈亏 {t['profit']:+.2f} 元")

# ============ 6. 绘图 ============
fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True,
                         gridspec_kw={"height_ratios": [3, 1]})

# 上图: 价格 + 均线 + 买卖点
ax1 = axes[0]
ax1.plot(df["date"], df["close"], label="收盘价", color="black", linewidth=1)
ax1.plot(df["date"], df["ma_short"], label=f"MA{SHORT_WINDOW}", color="orange", linewidth=1)
ax1.plot(df["date"], df["ma_long"], label=f"MA{LONG_WINDOW}", color="blue", linewidth=1)

buy_pts = df[df["signal"] == 1]
sell_pts = df[df["signal"] == -1]
ax1.scatter(buy_pts["date"], buy_pts["close"], marker="^", color="red", s=80, label="买入", zorder=5)
ax1.scatter(sell_pts["date"], sell_pts["close"], marker="v", color="green", s=80, label="卖出", zorder=5)

ax1.set_title(f"{STOCK_CODE} 均线金叉策略回测 ({START_DATE} ~ {END_DATE})")
ax1.set_ylabel("价格 (元)")
ax1.legend(loc="best")
ax1.grid(alpha=0.3)

# 下图: 资金曲线
ax2 = axes[1]
ax2.plot(df["date"], df["equity"], label="策略资金曲线", color="purple", linewidth=1.2)
ax2.axhline(INIT_CASH, color="gray", linestyle="--", linewidth=1, label="初始资金")
ax2.set_ylabel("总资产 (元)")
ax2.set_xlabel("日期")
ax2.legend(loc="best")
ax2.grid(alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.tight_layout()
plt.savefig("ma_cross_backtest.png", dpi=120)
plt.show()
print("\n图表已保存为 ma_cross_backtest.png")