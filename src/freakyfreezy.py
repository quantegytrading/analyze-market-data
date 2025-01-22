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


def append_with_letters(list, letter) -> []:
    return [f'{x} ({letter})' for x in list]


def frequency_of_buys_sells(head, tail, ret_val=[], frequency=1) -> list:
    if not tail:
        ret_val.append(f'{head} ({frequency})')
        return ret_val
    if head in tail:
        frequency += 1
        head, *tail = tail
        ret_val = frequency_of_buys_sells(head, tail, ret_val, frequency)
        return ret_val

    else:
        ret_val.append(f'{head} ({frequency})')
        head, *tail = tail
        ret_val = frequency_of_buys_sells(head, tail, ret_val, 1)
        return ret_val
    

def freakyfreezy(symbol, data) -> BuysSells:
    # apollonia_bs = apollonia(symbol, data)
    apollonia_bs = BuysSells([],[])
    bauhaus_bs = bauhaus(symbol, data)
    carini_bs = carini(symbol, data)
    dangermouse_bs = dangermouse(symbol, data)
    evangeline_bs = evangeline(symbol, data)
    # buys = append_with_letters(apollonia_bs.buys, "A") + append_with_letters(bauhaus_bs.buys, "B") + append_with_letters(carini_bs.buys, "C") + append_with_letters(dangermouse_bs.buys, "D") + append_with_letters(evangeline_bs.buys, "E")
    # sells = append_with_letters(apollonia_bs.sells, "A") + append_with_letters(bauhaus_bs.sells, "B") + append_with_letters(carini_bs.sells, "C") + append_with_letters(dangermouse_bs.sells, "D") + append_with_letters(evangeline_bs.sells, "E")

    buys =  apollonia_bs.buys + bauhaus_bs.buys + carini_bs.buys + dangermouse_bs.buys + evangeline_bs.buys
    sells = apollonia_bs.sells + bauhaus_bs.sells + carini_bs.sells + dangermouse_bs.sells + evangeline_bs.sells
    print("Full Buys: " + str(buys))
    print("full sells: " + str(sells))

    if len(buys) > 0:
        for buy in buys:
            if buy in sells:
                buys.remove(buy)
                sells.remove(buy)
        head, *tail = sorted(buys)
        buys = frequency_of_buys_sells(head=head, tail=tail, ret_val=[], frequency=1)
    if len(sells) > 0:
        head, *tail = sorted(sells)
        sells = frequency_of_buys_sells(head=head, tail=tail, ret_val=[], frequency=1)
    ff = BuysSells(buys, sells)

    # print("Apollonia Buys: " + str(apollonia_bs.buys))
    # print("Bauhaus Buys: " + str(bauhaus_bs.buys))
    # print("Carini Buys: " + str(carini_bs.buys))
    # print("Dangermouse Buys: " + str(dangermouse_bs.buys))
    # print("Evangeline Buys: " + str(evangeline_bs.buys))
    # print("Apollonia Sells: " + str(apollonia_bs.sells))
    # print("Bauhaus Sells: " + str(bauhaus_bs.sells))
    # print("Carini Sells: " + str(carini_bs.sells))
    # print("Dangermouse Sells: " + str(dangermouse_bs.sells))
    # print("Evangeline Sells: " + str(evangeline_bs.sells))
    print("Buys: " + str(ff.buys))
    print("Sells: " + str(ff.sells))
    return ff


def main(event, context):
    algorithm = "freakyfreezy"
    go(event, algorithm, freakyfreezy)


if __name__ == "__main__":
    main('', '')
