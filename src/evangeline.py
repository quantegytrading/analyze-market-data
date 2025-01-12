from common import go, get_all_candle_packages
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
import pandas as pd
import datetime
from domain.objects import BuysSells
from indicators.fibonacci import bullish_fibonacci, bearish_fibonacci


def evangeline(symbol, data) -> BuysSells:
    buys = []
    sells = []
    non_tradables = ['USDT', 'BNB', 'USDC']
    pddf = pd.DataFrame.from_records(data=data, columns=["date", "open", "high", "low", "close", "volume"])
    pddf.set_index("date", inplace=True)
    stock = sdf.retype(pddf)
    boll_ub = stock.get('boll_ub')
    boll_lb = stock.get('boll_lb')
    recent_upper_bollinger_band = boll_ub[-1:].values
    recent_lower_bollinger_band = boll_lb[-1:].values
    data.reverse()
    candles = get_all_candle_packages(symbol, data)
    print("Current Time: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    for candle in candles:
        print(str(candle.dt))
        print(symbol + ": " + datetime.datetime.fromtimestamp(int(candle.dt)/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
    if candles[0].c < recent_lower_bollinger_band[0] and \
            bullish_fibonacci(candles) and \
            symbol not in non_tradables:  # Dont buy USDT or BNB
        sells.append(symbol)
    elif candles[0].c > recent_upper_bollinger_band[0] and \
            bearish_fibonacci(candles) and \
            symbol not in non_tradables:  # Dont sell USDT or BNB
        buys.append(symbol)

    return BuysSells(buys, sells)


def main(event, context):
    algorithm = "evangeline"
    go(event, algorithm, evangeline)


if __name__ == "__main__":
    main('', '')
