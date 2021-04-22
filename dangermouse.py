from decimal import Decimal

from common import go
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
import pandas as pd

from domain.objects import BuysSells


def dangermouse(symbol, data) -> BuysSells:
    buys = []
    sells = []
    pddf = pd.DataFrame.from_records(data=data, columns=["date", "open", "high", "low", "close", "volume"])
    pddf.set_index("date", inplace=True)
    stock = sdf.retype(pddf)
    rsi = stock.get('rsi_6')
    print("rsi")
    print(rsi)
    rsi_last_2 = rsi[-2:].values.tolist()
    print(symbol)
    print(rsi_last_2)
    this_period = Decimal(rsi_last_2[1])
    last_period = Decimal(rsi_last_2[0])
    print("this_period: " + str(this_period))
    print("last_period: " + str(last_period))
    if this_period > 70:
        buys.append(symbol)
    elif this_period < 30:
        sells.append(symbol)
    # vd = stock['volume_delta']
    # print("-------------------" + symbol + " macd----------------------")
    # print(vd)
    print("------buys---------")
    print(buys)
    print("------sells---------")
    print(sells)
    return BuysSells(buys, sells)


def main(event, context):
    algorithm = "dangermouse"
    go(event, algorithm, dangermouse)


if __name__ == "__main__":
    main('', '')
