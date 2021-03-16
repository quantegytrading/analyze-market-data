# apollonia.py
from analyze import bullish_patterns_present, bearish_patterns_present


def apollonia(ccc):
    buys = []
    sells = []

    if bullish_patterns_present(ccc):
        symbol = ccc.candle1.c
        buys.append(symbol)
    if bearish_patterns_present(ccc):
        sells.append(symbol)
    return buys
