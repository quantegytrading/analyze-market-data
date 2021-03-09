# handler.py
import json
from dataclasses import dataclass

import boto3


@dataclass
class Candle:
    def __init__(self, dt: str, s: str, o: float, h: float, l: float, c: float, u: str):
        self.s = s
        self.o = o
        self.c = c
        self.h = h
        self.l = l
        self.dt = dt
        self.u = u


class TwoCandles:
    def __init__(self, candle1: Candle, candle2: Candle):
        self.candle1 = candle1
        self.candle2 = candle2


class ThreeCandles:
    def __init__(self, candle1: Candle, candle2: Candle, candle3: Candle):
        self.candle1 = candle1
        self.candle2 = candle2
        self.candle3 = candle3


def green(candle):
    return candle.c >= candle.o


def red(candle):
    return candle.o > candle.c


def lower_wick(green, candle):
    if green:
        return candle.o - candle.l
    else:
        return candle.c - candle.l


def upper_wick(green, candle):
    if green:
        return candle.h - candle.c
    else:
        return candle.h - candle.o


def body_size(green, candle):
    if green:
        return candle.c - candle.o
    else:
        return candle.o - candle.c


def white_soldiers(ccc):
    if green(ccc.candle1):
        if green(ccc.candle2):
            if green(ccc.candle3):
                if ccc.candle1.o > ccc.candle2.o:
                    if ccc.candle2.o > ccc.candle3.o:
                        if ccc.candle1.c > ccc.candle2.c:
                            if ccc.candle2.c > ccc.candle3.c:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def bullish_harami(ccc):
    if green(ccc.candle1):
        if red(ccc.candle2):
            if ccc.candle1.o > ccc.candle2.c:
                if ccc.candle1.c < ccc.candle2.o:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def inverted_hammer(candle):
    if green(candle):
        if upper_wick(True, candle) >= (body_size(True, candle) * 2):
            if lower_wick(True, candle) <= (body_size(True, candle) * .5):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def hammer(candle):
    if green(candle):
        if lower_wick(True, candle) >= (body_size(True, candle) * 2):
            if upper_wick(True, candle) <= (body_size(True, candle) * .5):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def hanging_man(candle):
    if red(candle):  # Red
        if lower_wick(False, candle) >= (body_size(False, candle) * 2):  # big lower wick
            if upper_wick(False, candle) <= (body_size(False, candle) * .5):  # small upper wick
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def shooting_star(candle):
    if red(candle):
        if upper_wick(False, candle) >= (body_size(False, candle) * 2):  # big upper wick
            if lower_wick(False, candle) <= (body_size(False, candle) * .5):  # small lower wick
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def black_crows(compound):
    if red(compound.candle1):
        if red(compound.candle2):
            if red(compound.candle3):
                if compound.candle1.o < compound.candle2.o:
                    if compound.candle2.o < compound.candle3.o:
                        if compound.candle1.c < compound.candle2.c:
                            if compound.candle2.c < compound.candle3.c:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def bearish_harami(compound):
    if red(compound.candle1):
        if green(compound.candle2):
            if compound.candle1.o < compound.candle2.c:
                if compound.candle1.c > compound.candle2.o:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def bullish_patterns_present(ccc):
    return \
        hammer(ccc.candle1) | \
        inverted_hammer(ccc.candle1) | \
        white_soldiers(ccc) | \
        bullish_harami(ccc)


def bearish_patterns_present(ccc):
    return \
        hanging_man(ccc.candle1) | \
        shooting_star(ccc.candle1) | \
        black_crows(ccc) | \
        bearish_harami(ccc)


def main(event, context):
    sns = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    buys = []
    sells = []
    message = {}
    symbols_string = event['Records'][0]['Sns']['Message']
    symbols_string = symbols_string.lstrip('[')
    symbols_string = symbols_string.rstrip(']')
    symbols_string = symbols_string.replace('"', '')
    symbols_string.replace(" ", "")
    symbols = symbols_string.split(",")
    keys = []
    for symbol in symbols:
        sym_dic = {"symbol": symbol.strip()}
        keys.append(sym_dic)
    keys_dict = {"Keys": keys}
    responses = dynamodb.batch_get_item(
        RequestItems={
            'market-data': keys_dict
        })
    market_data: list = responses['Responses']["market-data"]
    for datum in market_data:
        s = datum['symbol']
        d = datum['data']
        print(datum)
        print(d)
        d_list = json.loads(d)
        print(d_list)
        if len(d_list) == 0:
            print("No data found for symbol: " + str(s))
        else:
            last_candles = d_list[-3:]
            print(last_candles)
            candle_data3 = last_candles[0]
            candle3 = Candle(candle_data3[0], s, candle_data3[1], candle_data3[2], candle_data3[3], candle_data3[4],
                             candle_data3[0])
            candle_data2 = last_candles[1]
            candle2 = Candle(candle_data2[0], s, candle_data2[1], candle_data2[2], candle_data2[3], candle_data2[4],
                             candle_data2[0])
            candle_data1 = last_candles[2]
            candle1 = Candle(candle_data1[0], s, candle_data1[1], candle_data1[2], candle_data1[3], candle_data1[4],
                             candle_data1[0])
            ccc = ThreeCandles(candle1, candle2, candle3)
            if bullish_patterns_present(ccc):
                buys.append(s)
            if bearish_patterns_present(ccc):
                sells.append(s)

    print("Buys: " + str(buys))
    print("sells: " + str(sells))
    message['buys'] = buys
    message['sells'] = sells
    sns.publish(
        TargetArn='arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-soak',
        Message=json.dumps(message)
    )


if __name__ == "__main__":
    main('', '')
