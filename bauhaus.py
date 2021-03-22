# apolloniabak.py

from common import go
from indicators.candlestick_patterns import *


def bauhaus(ccc):
    buys = []
    if hanging_man(ccc.candle1) or shooting_star(ccc.candle1) or black_crows(ccc) or bearish_harami(ccc):
        symbol = ccc.candle1.s
        buys.append(symbol)
    return buys


def main(event, context):

    algorithm = "bauhaus"
    go(event, algorithm, bauhaus)


if __name__ == "__main__":
    main('', '')
