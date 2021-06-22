def bullish_fibonacci(candles):
    ## For 8 candles
    for i in range(0, 7):
        candle = candles[i]
        if not candle.c < candles[i + 5].c or \
                not candle.c < candles[i + 3].c or \
                not candle.c < candles[i + 2].c or \
                not candle.c < candles[i + 1].c:
            return False
    return True


def bearish_fibonacci(candles):
        ## For 8 candles
        for i in range(0, 7):
            candle = candles[i]
            if not candle.c > candles[i + 5].c or \
                    not candle.c > candles[i + 3].c or \
                    not candle.c > candles[i + 2].c or \
                    not candle.c > candles[i + 1].c:
                return False
        return True
