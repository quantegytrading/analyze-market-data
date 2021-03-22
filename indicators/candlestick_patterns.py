from indicators.common import *


def white_soldiers(ccc):
    if green(ccc.candle1) and \
            green(ccc.candle2) and \
            green(ccc.candle3) and \
            ccc.candle1.o > ccc.candle2.o > ccc.candle3.o and \
            ccc.candle1.c > ccc.candle2.c > ccc.candle3.c:
        return True
    else:
        return False


def bullish_harami(ccc):
    if green(ccc.candle1) and \
            red(ccc.candle2) and \
            ccc.candle1.o > ccc.candle2.c and \
            ccc.candle1.c < ccc.candle2.o:
        return True
    else:
        return False


def inverted_hammer(candle):
    if green(candle) and \
            upper_wick(True, candle) >= (body_size(True, candle) * 2) and \
            lower_wick(True, candle) <= (body_size(True, candle) * .5):
        return True
    else:
        return False


def hammer(candle):
    if green(candle) and \
            lower_wick(True, candle) >= (body_size(True, candle) * 2) and \
            upper_wick(True, candle) <= (body_size(True, candle) * .5):
        return True
    else:
        return False


def hanging_man(candle):
    if red(candle) and \
            lower_wick(False, candle) >= (body_size(False, candle) * 2) and \
            upper_wick(False, candle) <= (body_size(False, candle) * .5):  # small upper wick
        return True
    else:
        return False


def shooting_star(candle):
    if red(candle):
        if upper_wick(False, candle) >= (body_size(False, candle) * 2):  # big upper wick
            if lower_wick(False, candle) <= (body_size(False, candle) * .5):  # small lower wick
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def black_crows(compound):
    if red(compound.candle1):
        if red(compound.candle2):
            if red(compound.candle3):
                if compound.candle1.o < compound.candle2.o:
                    if compound.candle2.o < compound.candle3.o:
                        if compound.candle1.c < compound.candle2.c:
                            if compound.candle2.c < compound.candle3.c:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def bearish_harami(compound):
    if red(compound.candle1):
        if green(compound.candle2):
            if compound.candle1.o < compound.candle2.c:
                if compound.candle1.c > compound.candle2.o:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
