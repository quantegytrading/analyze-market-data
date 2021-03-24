from common import go
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
import pandas as pd

from domain.objects import BuysSells


def carini(symbol, data) -> BuysSells:
    buys = []
    sells = []
    pddf = pd.DataFrame.from_records(data=data, columns=["date", "open", "high", "low", "close", "volume"])
    pddf.set_index("date", inplace=True)
    # print(pddf)
    stock = sdf.retype(pddf)
    macd = stock.get('macd')
    macd_last_2 = macd[-2:].values.tolist()
    print(macd_last_2)
    this_period = macd_last_2[1]
    last_period = macd_last_2[0]
    if this_period > 0 and last_period < 0:
        buys.append(symbol)
    elif this_period < 0 and last_period[0] > 0:
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
    algorithm = "carini"
    go(event, algorithm, carini)


if __name__ == "__main__":
    main('', '')
