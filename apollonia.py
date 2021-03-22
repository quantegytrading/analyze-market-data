# apollonia.py

from common import go
from indicators.candlestick_patterns import *


def apollonia(ccc):
    buys = []
    if hammer(ccc.candle1) | inverted_hammer(ccc.candle1) | white_soldiers(ccc) | bullish_harami(ccc):
        symbol = ccc.candle1.s
        buys.append(symbol)
    return buys


def main(event, context):
    algorithm = "apollonia"
    go(event, algorithm, apollonia)


if __name__ == "__main__":
    main('', '')
