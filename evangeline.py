from decimal import Decimal

from common import go
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
import pandas as pd

from domain.objects import BuysSells


def evangeline(symbol, data) -> BuysSells:
    buys = []
    sells = []
    pddf = pd.DataFrame.from_records(data=data, columns=["date", "open", "high", "low", "close", "volume"])
    pddf.set_index("date", inplace=True)
    stock = sdf.retype(pddf)
    boll_ub = stock.get('boll_ub')
    boll_lb = stock.get('boll_lb')

    print("boll_ub")
    print(boll_ub)
    print("boll_lb")
    print(boll_lb)

    return BuysSells(buys, sells)


def main(event, context):
    algorithm = "evangeline"
    go(event, algorithm, evangeline)


if __name__ == "__main__":
    main('', '')
