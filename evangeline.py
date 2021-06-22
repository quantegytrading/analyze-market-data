from decimal import Decimal

from common import go, get_all_candle_packages
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
import pandas as pd

from domain.objects import BuysSells
from indicators.fibonacci import bullish_fibonacci, bearish_fibonacci


def evangeline(symbol, data) -> BuysSells:
    buys = []
    sells = []
    pddf = pd.DataFrame.from_records(data=data, columns=["date", "open", "high", "low", "close", "volume"])
    pddf.set_index("date", inplace=True)
    stock = sdf.retype(pddf)
    boll_ub = stock.get('boll_ub')
    boll_lb = stock.get('boll_lb')

    recent_upper_bollinger_band = boll_ub[-1:].values
    recent_lower_bollinger_band = boll_lb[-1:].values
    print("recent_upper_bollinger_band")
    print(recent_upper_bollinger_band[0])
    print("recent_lower_bollinger_band")
    print(recent_lower_bollinger_band[0])
    print(data)
    data.reverse()
    print(data)
    candles = get_all_candle_packages(symbol, data)
    print(candles)
    bull_fib = bullish_fibonacci(candles)
    bear_fib = bearish_fibonacci(candles)
    print(bull_fib)
    print(bear_fib)

    if candles[0].c < recent_lower_bollinger_band[0] and bull_fib:
        buys.append(symbol)
    elif candles[0].c > recent_upper_bollinger_band[0] and bear_fib:
        sells.append(symbol)

    return BuysSells(buys, sells)


def main(event, context):
    algorithm = "evangeline"
    go(event, algorithm, evangeline)


if __name__ == "__main__":
    main('', '')
