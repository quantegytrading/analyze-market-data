# apolloniabak.py

from common import go, get_candle_package
from domain.objects import BuysSells
from indicators.candlestick_patterns import *


def bauhaus(symbol, data) -> BuysSells:
    buys = []
    sells = []
    if len(data) == 0:
        print("No data found for symbol: " + str(symbol))
    else:
        last_candles = data[-3:]
        ccc = get_candle_package(symbol, last_candles)
        if hanging_man(ccc.candle1) or shooting_star(ccc.candle1) or black_crows(ccc) or bearish_harami(ccc):
            buys.append(symbol)
    return BuysSells(buys, sells)


def main(event, context):

    algorithm = "bauhaus"
    go(event, algorithm, bauhaus)


if __name__ == "__main__":
    main('', '')
