def bullish_fibonacci(candles):
    for i in range(0, 7):
        candle = candles[i]
        print("close -5 -3 -2 -1")
        print(str(candle.c) + " " + str(candles[i + 5].c) + " " + str(candles[i + 3].c) + " " + str(candles[i + 2].c) + " " + str(candles[i + 1].c))
        if candle.c < candles[i + 5].c and \
                candle.c < candles[i + 3].c and \
                candle.c < candles[i + 2].c and \
                candle.c < candles[i + 1].c:
            return True
    return False


def bearish_fibonacci(candles):
    for i in range(0, 7):
        candle = candles[i]
        print(str(candle.c) + " " + str(candles[i + 5].c) + " " + str(candles[i + 3].c) + " " + str(candles[i + 2].c) + " " + str(candles[i + 1].c))
        if candle.c > candles[i + 5].c and \
                candle.c > candles[i + 3].c and \
                candle.c > candles[i + 2].c and \
                candle.c > candles[i + 1].c:
            return True
    return False
