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
    bub_last_2 = boll_ub[-2:].values.tolist()
    blb_last_2 = boll_lb[-2:].values.tolist()
    print(symbol)
    print(data)
    print(stock)
    print(pddf)
    print(bub_last_2)
    print(blb_last_2)
    this_period = Decimal(bub_last_2[1])
    last_period = Decimal(bub_last_2[0])
    lthis_period = Decimal(blb_last_2[1])
    llast_period = Decimal(blb_last_2[0])
    print("this_period: " + str(this_period))
    print("lthis_period: " + str(lthis_period))
    print("last_period: " + str(last_period))
    print("llast_period: " + str(llast_period))
    return BuysSells(buys, sells)


def main(event, context):
    algorithm = "evangeline"
    go(event, algorithm, evangeline)


if __name__ == "__main__":
    main('', '')
