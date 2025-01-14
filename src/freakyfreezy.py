from common import go, get_all_candle_packages
# from indicators.candlestick_patterns import *
from stockstats import StockDataFrame as sdf
from appollonia import appolonia
from bauhaus import bauhaus
from carini import carini
from dangermouse import dangermouse
from evangeline import evangeline
import pandas as pd
import datetime
from domain.objects import BuysSells
from indicators.fibonacci import bullish_fibonacci, bearish_fibonacci


def freakyfreezy(symbol, data) -> BuysSells:
    appolonia_bs = appolonia(symbol, data)
    bauhaus_bs = bauhaus(symbol, data)
    carini_bs = carini(symbol, data)
    dangermouse_bs = dangermouse(symbol, data)
    evangeline_bs = evangeline(symbol, data)
    buys = appolonia_bs.buys + bauhaus_bs.buys + carini_bs.buys + dangermouse_bs.buys + evangeline_bs.buys
    sells = appolonia_bs.sells + bauhaus_bs.sells + carini_bs.sells + dangermouse_bs.sells + evangeline_bs.sells
    ff = BuysSells(set(buys), set(sells))
    print("Appolonia Buys: " + str(appolonia_bs.buys))
    print("Bauhaus Buys: " + str(bauhaus_bs.buys))
    print("Carini Buys: " + str(carini_bs.buys))
    print("Dangermouse Buys: " + str(dangermouse_bs.buys))
    print("Evangeline Buys: " + str(evangeline_bs.buys))
    print("Appolonia Sells: " + str(appolonia_bs.sells))
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
