# apollonia.py

from common import common
from analyze import bullish_patterns_present, bearish_patterns_present


def apollonia(ccc):
    buys = []
    symbol = ""
    if bullish_patterns_present(ccc):
        symbol = ccc.candle1.s
        buys.append(symbol)
    # if bearish_patterns_present(ccc):
    return buys


def main(event, context):
    algorithm = "apollonia"
    common(event, algorithm, apollonia)


if __name__ == "__main__":
    main('', '')
