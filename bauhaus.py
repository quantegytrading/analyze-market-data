# bauhaus.py
from analyze import bullish_patterns_present, bearish_patterns_present


def bauhaus(ccc):
    buys = []
    sells = []
    if bullish_patterns_present(ccc):
        symbol = ccc.candle1.c
        sells.append(symbol)
    if bearish_patterns_present(ccc):
        buys.append(symbol)
    return buys, sells
