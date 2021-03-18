# apollonia.py

from common import go
from analyze import bullish_patterns_present, bearish_patterns_present


def apollonia(ccc):
    buys = []
    if bullish_patterns_present(ccc):
        symbol = ccc.candle1.s
        buys.append(symbol)
    return buys


def main(event, context):
    algorithm = "apollonia"
    go(event, algorithm, apollonia)


if __name__ == "__main__":
    main('', '')
