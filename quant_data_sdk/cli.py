"""
quant-data 命令行工具

用法：
    quant-data stock realtime 600519
    quant-data stock kline 600519 --start 2024-01-01 --end 2024-12-31
    quant-data market stats
    quant-data sector performance
    quant-data ai generate "写一个双均线策略" -o backtest.py
"""

import argparse
import json
import sys
from typing import List

from .client import QuantDataClient
from .exceptions import QuantDataError


def _print(data, output: str = None, as_json: bool = False):
    """输出数据"""
    if output:
        if output.endswith(".json"):
            with open(output, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif output.endswith(".csv"):
            from .utils import to_dataframe
            df = to_dataframe(data)
            df.to_csv(output, index=False, encoding="utf-8-sig")
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(str(data))
        print(f"✅ 已保存到 {output}")
        return

    print(json.dumps(data, ensure_ascii=False, indent=2))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quant-data",
        description="A 股量化数据命令行工具",
    )
    parser.add_argument("--api-key", help="API Key（不传则匿名）")
    parser.add_argument("--base-url", default="https://zizhenghua.com/api",
                        help="API 基础地址")
    parser.add_argument("--json", action="store_true", help="JSON 输出")

    sub = parser.add_subparsers(dest="command", required=True)

    # ===== stock =====
    stock = sub.add_parser("stock", help="个股接口")
    stock_sub = stock.add_subparsers(dest="subcommand", required=True)

    p = stock_sub.add_parser("realtime", help="实时行情")
    p.add_argument("code", nargs="+", help="股票代码")

    p = stock_sub.add_parser("kline", help="K 线")
    p.add_argument("code", help="股票代码")
    p.add_argument("--start", help="起始日期 YYYY-MM-DD")
    p.add_argument("--end", help="结束日期 YYYY-MM-DD")

    p = stock_sub.add_parser("ranking", help="涨幅榜")
    p.add_argument("--refresh", action="store_true")

    p = stock_sub.add_parser("losers", help="跌幅榜")
    p.add_argument("--refresh", action="store_true")

    p = stock_sub.add_parser("turnover", help="换手率榜")
    p.add_argument("--refresh", action="store_true")

    p = stock_sub.add_parser("filter", help="选股")
    p.add_argument("--min-turnover", type=float)
    p.add_argument("--min-roe", type=float)
    p.add_argument("--min-volume-ratio", type=float)
    p.add_argument("--sort-by", default="volumeRatio")
    p.add_argument("--limit", type=int, default=20)

    # ===== market =====
    market = sub.add_parser("market", help="市场接口")
    market_sub = market.add_subparsers(dest="subcommand", required=True)
    p = market_sub.add_parser("stats", help="市场统计")
    p.add_argument("--refresh", action="store_true")
    p = market_sub.add_parser("histogram", help="涨跌幅分布")
    p.add_argument("--refresh", action="store_true")
    p = market_sub.add_parser("volume-spike", help="量比异动榜")
    p.add_argument("--refresh", action="store_true")
    p = market_sub.add_parser("amplitude", help="振幅极端榜")
    p.add_argument("--refresh", action="store_true")

    # ===== sector =====
    sector = sub.add_parser("sector", help="行业接口")
    sector_sub = sector.add_subparsers(dest="subcommand", required=True)
    p = sector_sub.add_parser("performance", help="行业涨跌幅")
    p.add_argument("--refresh", action="store_true")
    p = sector_sub.add_parser("amount", help="行业成交额排行")
    p.add_argument("--refresh", action="store_true")

    # ===== fin =====
    fin = sub.add_parser("fin", help="财务接口")
    fin_sub = fin.add_subparsers(dest="subcommand", required=True)
    p = fin_sub.add_parser("latest", help="最新财务指标")
    p.add_argument("code")
    p = fin_sub.add_parser("history", help="财务历史")
    p.add_argument("code")
    p.add_argument("-n", type=int, default=8)
    p = fin_sub.add_parser("top-roe", help="ROE 排名")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--min-roe", type=float, default=0)

    # ===== factor =====
    factor = sub.add_parser("factor", help="多因子接口")
    factor_sub = factor.add_subparsers(dest="subcommand", required=True)
    p = factor_sub.add_parser("ranking", help="多因子排名")
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--refresh", action="store_true")

    # ===== ai =====
    ai = sub.add_parser("ai", help="AI 接口")
    ai_sub = ai.add_subparsers(dest="subcommand", required=True)
    p = ai_sub.add_parser("generate", help="生成策略代码")
    p.add_argument("prompt", help="自然语言描述")
    p.add_argument("--language", default="python", choices=["python", "java"])

    return parser


def _extract_output(argv: List[str]):
    """
    从 argv 里手动提取 -o / --output（支持放任意位置）

    返回 (output, new_argv)
    """
    output = None
    new_argv = []
    i = 0
    while i < len(argv):
        if argv[i] in ("-o", "--output"):
            if i + 1 < len(argv):
                output = argv[i + 1]
                i += 2
                continue
        elif argv[i].startswith("--output="):
            output = argv[i].split("=", 1)[1]
            i += 1
            continue
        new_argv.append(argv[i])
        i += 1
    return output, new_argv


def main(argv: List[str] = None):
    if argv is None:
        argv = sys.argv[1:]

    # 手动提取 -o（支持放任意位置）
    output, argv = _extract_output(argv)

    parser = _build_parser()
    args = parser.parse_args(argv)
    args.output = output

    client = QuantDataClient(
        api_key=args.api_key,
        base_url=args.base_url,
    )

    try:
        # ===== stock =====
        if args.command == "stock":
            if args.subcommand == "realtime":
                if len(args.code) == 1:
                    data = client.stock.get_realtime(args.code[0])
                else:
                    data = [client.stock.get_realtime(c) for c in args.code]
            elif args.subcommand == "kline":
                data = client.stock.get_kline(args.code, args.start, args.end)
            elif args.subcommand == "ranking":
                data = client.stock.get_ranking(args.refresh)
            elif args.subcommand == "losers":
                data = client.stock.get_losers(args.refresh)
            elif args.subcommand == "turnover":
                data = client.stock.get_turnover_ranking(args.refresh)
            elif args.subcommand == "filter":
                filters = {}
                if args.min_turnover is not None:
                    filters["minTurnover"] = args.min_turnover
                if args.min_roe is not None:
                    filters["minRoe"] = args.min_roe
                if args.min_volume_ratio is not None:
                    filters["minVolumeRatio"] = args.min_volume_ratio
                filters["sortBy"] = args.sort_by
                filters["limit"] = args.limit
                data = client.stock.filter_stocks(**filters)
            else:
                parser.error(f"未知子命令: {args.subcommand}")

        # ===== market =====
        elif args.command == "market":
            if args.subcommand == "stats":
                data = client.market.get_stats(args.refresh)
            elif args.subcommand == "histogram":
                data = client.market.get_histogram(args.refresh)
            elif args.subcommand == "volume-spike":
                data = client.market.get_volume_spike(args.refresh)
            elif args.subcommand == "amplitude":
                data = client.market.get_amplitude_extreme(args.refresh)
            else:
                parser.error(f"未知子命令: {args.subcommand}")

        # ===== sector =====
        elif args.command == "sector":
            if args.subcommand == "performance":
                data = client.sector.get_performance(args.refresh)
            elif args.subcommand == "amount":
                data = client.sector.get_amount_ranking(args.refresh)
            else:
                parser.error(f"未知子命令: {args.subcommand}")

        # ===== fin =====
        elif args.command == "fin":
            if args.subcommand == "latest":
                data = client.fin.get_latest(args.code)
            elif args.subcommand == "history":
                data = client.fin.get_history(args.code, args.n)
            elif args.subcommand == "top-roe":
                data = client.fin.get_top_roe(args.limit, args.min_roe)
            else:
                parser.error(f"未知子命令: {args.subcommand}")

        # ===== factor =====
        elif args.command == "factor":
            if args.subcommand == "ranking":
                data = client.factor.get_ranking(args.top, args.refresh)
            else:
                parser.error(f"未知子命令: {args.subcommand}")

        # ===== ai =====
        elif args.command == "ai":
            if args.subcommand == "generate":
                result = client.ai.generate_code(args.prompt, args.language)
                code = client.ai.extract_code(result["raw"], args.language)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(code)
                    print(f"✅ 已保存到 {args.output}")
                else:
                    print(code)
                return
            else:
                parser.error(f"未知子命令: {args.subcommand}")

        else:
            parser.error(f"未知命令: {args.command}")

        _print(data, args.output, args.json)

    except QuantDataError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()