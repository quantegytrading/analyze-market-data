# apolloniabak.py

from common import go
from analyze import bullish_patterns_present, bearish_patterns_present


def bauhaus(ccc):
    buys = []
    if bearish_patterns_present(ccc):
        symbol = ccc.candle1.s
        buys.append(symbol)
    return buys


def main(event, context):

    algorithm = "bauhaus"
    go(event, algorithm, bauhaus)


if __name__ == "__main__":
    main('', '')
