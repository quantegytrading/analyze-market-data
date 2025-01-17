from common import go, get_all_candle_packages
from apollonia import apollonia
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
from bauhaus import bauhaus
from carini import carini
from dangermouse import dangermouse
from evangeline import evangeline
import pandas as pd
import datetime
from domain.objects import BuysSells
from indicators.fibonacci import bullish_fibonacci, bearish_fibonacci


def freakyfreezy(symbol, data) -> BuysSells:
    apollonia_bs = apollonia(symbol, data)
    bauhaus_bs = bauhaus(symbol, data)
    carini_bs = carini(symbol, data)
    dangermouse_bs = dangermouse(symbol, data)
    evangeline_bs = evangeline(symbol, data)
    buys = apollonia_bs.buys + bauhaus_bs.buys + carini_bs.buys + dangermouse_bs.buys + evangeline_bs.buys
    sells = apollonia_bs.sells + bauhaus_bs.sells + carini_bs.sells + dangermouse_bs.sells + evangeline_bs.sells
    print("Full Buys: " + str(buys))
    print("Full Sells: " + str(sells))
    ff = BuysSells(set(buys), set(sells))
    print("Apollonia Buys: " + str(apollonia_bs.buys))
    print("Bauhaus Buys: " + str(bauhaus_bs.buys))
    print("Carini Buys: " + str(carini_bs.buys))
    print("Dangermouse Buys: " + str(dangermouse_bs.buys))
    print("Evangeline Buys: " + str(evangeline_bs.buys))
    print("Apollonia Sells: " + str(apollonia_bs.sells))
    print("Bauhaus Sells: " + str(bauhaus_bs.sells))
    print("Carini Sells: " + str(carini_bs.sells))
    print("Dangermouse Sells: " + str(dangermouse_bs.sells))
    print("Evangeline Sells: " + str(evangeline_bs.sells))
    print("Buys: " + str(ff.buys))
    print("Sells: " + str(ff.sells))
    return ff


def main(event, context):
    algorithm = "freakyfreezy"
    go(event, algorithm, freakyfreezy)


if __name__ == "__main__":
    main('', '')
