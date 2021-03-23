from common import go
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
import pandas as pd


def carini(symbol, data):
    buys = []
    pddf = pd.DataFrame.from_records(data=data, columns=["date", "open", "high", "low", "close", "volume"])
    pddf.set_index("date", inplace=True)
    print(pddf)
    stock = sdf.retype(pddf)
    macd = stock.get('macd')
    vd = stock['volume_delta']
    print("-------------------" + symbol + " macd----------------------")
    print(macd)
    print(vd)
    return buys


def main(event, context):
    algorithm = "carini"
    go(event, algorithm, carini)


if __name__ == "__main__":
    main('', '')
