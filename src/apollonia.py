# apollonia.py

from common import go, get_candle_package
from .domain.objects import BuysSells
from .indicators.candlestick_patterns import *


def apollonia(symbol, data) -> BuysSells:
    buys = []
    sells = []
    if len(data) == 0:
        print("No data found for symbol: " + str(symbol))
    else:
        last_candles = data[-3:]
        ccc = get_candle_package(symbol, last_candles)
        if hammer(ccc.candle1) | inverted_hammer(ccc.candle1) | white_soldiers(ccc) | bullish_harami(ccc):
            symbol = ccc.candle1.s
            buys.append(symbol)
    return BuysSells(buys, sells)


def main(event, context):
    print(event)
    algorithm = "apollonia"
    go(event, algorithm, apollonia)


if __name__ == "__main__":
    main('', '')
