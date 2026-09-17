import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体，避免绘图乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


# ==================== 1. 数据获取 ====================
def get_stock_data(symbol="600519", start_date="2023-01-01", end_date="2025-12-31"):
    """
    使用 akshare 获取股票日线数据
    symbol: 股票代码，600519 为贵州茅台
    """
    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date.replace("-", ""),
        end_date=end_date.replace("-", ""),
        adjust="qfq"  # 前复权
    )
    # 重命名列
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
    return df


# ==================== 2. 布林带策略 ====================
def bollinger_strategy(df, window=20, num_std=2):
    """
    布林带策略：
    - 价格跌破下轨 -> 买入
    - 价格突破上轨 -> 卖出
    """
    df = df.copy()
    # 计算中轨（移动平均）
    df["ma"] = df["close"].rolling(window=window).mean()
    # 计算标准差
    df["std"] = df["close"].rolling(window=window).std()
    # 上轨、下轨
    df["upper"] = df["ma"] + num_std * df["std"]
    df["lower"] = df["ma"] - num_std * df["std"]

    # 生成信号：1 买入，-1 卖出，0 持有
    df["signal"] = 0
    df.loc[df["close"] < df["lower"], "signal"] = 1   # 跌破下轨买入
    df.loc[df["close"] > df["upper"], "signal"] = -1  # 突破上轨卖出

    return df


# ==================== 3. 回测执行 ====================
def backtest(df, initial_capital=100000):
    """
    逐日循环回测
    """
    df = df.copy()
    cash = initial_capital
    position = 0  # 持股数量
    trades = []   # 交易记录
    equity_curve = []  # 每日总资产

    for i in range(len(df)):
        price = df.loc[i, "close"]
        signal = df.loc[i, "signal"]

        # 买入信号：空仓时全仓买入
        if signal == 1 and position == 0:
            position = cash // price  # 按手数买入（A股100股一手，这里简化）
            if position > 0:
                cost = position * price
                cash -= cost
                trades.append({
                    "date": df.loc[i, "date"],
                    "type": "buy",
                    "price": price,
                    "shares": position
                })

        # 卖出信号：持仓时全部卖出
        elif signal == -1 and position > 0:
            revenue = position * price
            cash += revenue
            trades.append({
                "date": df.loc[i, "date"],
                "type": "sell",
                "price": price,
                "shares": position
            })
            position = 0

        # 记录每日总资产
        total = cash + position * price
        equity_curve.append(total)

    df["equity"] = equity_curve
    return df, trades, cash, position


# ==================== 4. 收益统计 ====================
def calc_stats(df, trades, initial_capital=100000):
    """
    计算收益率、最大回撤、胜率、交易次数
    """
    final_equity = df["equity"].iloc[-1]
    total_return = (final_equity - initial_capital) / initial_capital

    # 最大回撤
    equity = df["equity"]
    cummax = equity.cummax()
    drawdown = (equity - cummax) / cummax
    max_drawdown = drawdown.min()

    # 配对交易计算胜率
    buy_price = None
    wins = 0
    total_trades = 0
    for t in trades:
        if t["type"] == "buy":
            buy_price = t["price"]
        elif t["type"] == "sell" and buy_price is not None:
            total_trades += 1
            if t["price"] > buy_price:
                wins += 1
            buy_price = None

    win_rate = wins / total_trades if total_trades > 0 else 0

    print("=" * 50)
    print("布林带回测结果")
    print("=" * 50)
    print(f"初始资金:       {initial_capital:.2f} 元")
    print(f"期末资产:       {final_equity:.2f} 元")
    print(f"总收益率:       {total_return * 100:.2f}%")
    print(f"最大回撤:       {max_drawdown * 100:.2f}%")
    print(f"交易次数:       {total_trades} 次")
    print(f"胜率:           {win_rate * 100:.2f}%")
    print("=" * 50)

    return {
        "total_return": total_return,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "total_trades": total_trades
    }


# ==================== 5. 绘图 ====================
def plot_result(df, trades):
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # 上图：价格 + 布林带 + 买卖点
    ax1 = axes[0]
    ax1.plot(df["date"], df["close"], label="收盘价", color="black", linewidth=1)
    ax1.plot(df["date"], df["ma"], label="中轨(MA20)", color="blue", linewidth=1)
    ax1.plot(df["date"], df["upper"], label="上轨", color="red", linestyle="--", linewidth=1)
    ax1.plot(df["date"], df["lower"], label="下轨", color="green", linestyle="--", linewidth=1)

    # 标记买卖点
    for t in trades:
        if t["type"] == "buy":
            ax1.scatter(t["date"], t["price"], marker="^", color="red", s=100, zorder=5)
        else:
            ax1.scatter(t["date"], t["price"], marker="v", color="green", s=100, zorder=5)

    ax1.set_title("贵州茅台 布林带策略回测")
    ax1.set_ylabel("价格 (元)")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # 下图：资产曲线
    ax2 = axes[1]
    ax2.plot(df["date"], df["equity"], label="账户总资产", color="purple")
    ax2.axhline(y=100000, color="gray", linestyle="--", label="初始资金")
    ax2.set_ylabel("资产 (元)")
    ax2.set_xlabel("日期")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("bollinger_backtest.png", dpi=100)
    plt.show()


# ==================== 主程序 ====================
if __name__ == "__main__":
    # 1. 获取数据
    df = get_stock_data(symbol="600519", start_date="2023-01-01", end_date="2025-12-31")
    print(f"数据条数: {len(df)}")

    # 2. 计算布林带
    df = bollinger_strategy(df, window=20, num_std=2)

    # 3. 回测
    df, trades, cash, position = backtest(df, initial_capital=100000)

    # 4. 统计
    stats = calc_stats(df, trades, initial_capital=100000)

    # 5. 绘图
    plot_result(df, trades)