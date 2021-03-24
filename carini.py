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
    macd_last_2 = macd[-2:]
    if macd_last_2[1] > 0:
        if macd_last_2[0] < 0:
            buys.append(symbol)
    elif macd_last_2[1] < 0:
        if macd_last_2[0] > 0:
            sells.append(symbol)
    # vd = stock['volume_delta']
    print("-------------------" + symbol + " macd----------------------")
    print(macd_last_2)
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
