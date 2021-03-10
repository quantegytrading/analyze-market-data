def green(candle):
    return candle.c >= candle.o


def red(candle):
    return candle.o > candle.c


def lower_wick(green, candle):
    if green:
        return candle.o - candle.l
    else:
        return candle.c - candle.l


def upper_wick(green, candle):
    if green:
        return candle.h - candle.c
    else:
        return candle.h - candle.o


def body_size(green, candle):
    if green:
        return candle.c - candle.o
    else:
        return candle.o - candle.c