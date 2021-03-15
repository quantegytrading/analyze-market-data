from indicators.candlestick_patterns import *


def bullish_patterns_present(ccc):
    return \
        hammer(ccc.candle1) | \
        inverted_hammer(ccc.candle1) | \
        white_soldiers(ccc) | \
        bullish_harami(ccc)


def bearish_patterns_present(ccc):
    return \
        hanging_man(ccc.candle1) | \
        shooting_star(ccc.candle1) | \
        black_crows(ccc) | \
        bearish_harami(ccc)
