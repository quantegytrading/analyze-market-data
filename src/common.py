# apolloniabak.py
import json
import os

import boto3
from domain.objects import Candle, ThreeCandles
# from slack_sdk import WebClient


def get_all_candle_packages(symbol, candles):
    try:
        candle_list = []
        for c in candles:
            candle = Candle(c[0], symbol, c[1], c[2], c[3], c[4], c[0])
            candle_list.append(candle)
        return candle_list
    except IndexError as e:
        print("Exception thrown getting data for " + symbol)


def get_candle_package(symbol, candles):
    try:
        c3 = candles[0]
        c2 = candles[1]
        c1 = candles[2]
        candle3 = Candle(c3[0], symbol, c3[1], c3[2], c3[3], c3[4], c3[0])
        candle2 = Candle(c2[0], symbol, c2[1], c2[2], c2[3], c2[4], c2[0])
        candle1 = Candle(c1[0], symbol, c1[1], c1[2], c1[3], c1[4], c1[0])
        return ThreeCandles(candle1, candle2, candle3)
    except IndexError as e:
        print("Exception thrown getting data for " + symbol)


def frequency_of_buys_sells(head: object, tail: object, ret_val=None, frequency: object = 1) -> object | list:
    if ret_val is None:
        ret_val = []
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


def algos_of_buys_sells(buys, sells):
    buys_retval = []
    sells_retval  = []
    buys_w_algos = []
    sells_w_algos = []

    # extract symbol and algo
    for buy in buys:
        buys_w_algos.append((buy[:-4], buy[-2]))

    for sell in sells:
        sells_w_algos.append((sell[:-4], sell[-2]))

    # make buys dict
    buys_retval_dict = {}
    for buy_w_algo in buys_w_algos:
        algos = set()
        for buy_w_algo2 in buys_w_algos:
            if buy_w_algo[0] == buy_w_algo2[0]:
                algos.add(buy_w_algo2[1])
        buys_retval_dict[buy_w_algo[0]] = list(algos)

    # make sells dict
    sells_retval_dict = {}
    for sell_w_algo in sells_w_algos:
        algos = set()
        for sell_w_algo2 in sells_w_algos:
            if sell_w_algo[0] == sell_w_algo2[0]:
                algos.add(sell_w_algo2[1])
        sells_retval_dict[sell_w_algo[0]] = list(algos)

    # normalize buys list
    for buy in buys_retval_dict.keys():
        if buy not in sells_retval_dict.keys():
            buys_retval.append(f'{buy} {buys_retval_dict[buy]}')

    # normalize sells list
    for buy in sells_retval_dict.keys():
        if buy not in buys_retval_dict.keys():
            sells_retval.append(f'{buy} {sells_retval_dict[buy]}')

    return buys_retval, sells_retval


def go(event, algorithm, algorithm_fn):
    sqs = boto3.client('sqs')
    buys = []
    prices = {}
    sells = []
    event_message = json.loads(event['Records'][0]['body'])
    print(event_message)
    env = 'prod'
    data_type = event_message['data_type']
    exchange = event_message['exchange']
    interval = event_message['interval']
    market_data_list = event_message['market_data']
    backtesttime = ""
    try:
        for market_data in market_data_list:
            symbol = market_data['symbol']
            data = json.loads(market_data['data'])
            if len(data) != 0:
                print(market_data['data'])
                last_candles = data[-3:]
                ccc = get_candle_package(symbol, last_candles)
                bs = algorithm_fn(symbol, data)
                buys.append(bs.buys)
                sells.append(bs.sells)
                prices[symbol] = ccc.candle1.c
    except Exception as e:
        print(e)
    # flat_buys = []
    # for buy in buys:
    #     if buy:
    #         flat_buys.append(buy[0])
    # 
    # flat_sells = []
    # for sell in sells:
    #     if sell:
    #         flat_sells.append(sell[0])
    
    flat_buys = [item for sublist in buys for item in sublist]
    flat_sells = [item for sublist in sells for item in sublist]
    if len(flat_buys) > 0:
        for buy in flat_buys:
            if buy in flat_sells:
                flat_buys.remove(buy)
                flat_sells.remove(buy)
    flat_buys, flat_sells = algos_of_buys_sells(flat_buys, flat_sells)
    #     head, *tail = sorted(flat_buys)
    #     flat_buys = frequency_of_buys_sells(head=head, tail=tail, ret_val=[], frequency=1)
    # if len(flat_sells) > 0:
    #      head, *tail = sorted(flat_sells)
    #      flat_sells = frequency_of_buys_sells(head=head, tail=tail, ret_val=[], frequency=1)
        
    message = {
        'algorithm': algorithm,
        'env': env,
        'interval': interval,
        'buys': flat_buys,
        'prices': prices,
        'sells': flat_sells,
        'data_type': data_type,
        'exchange': exchange,
        'backtest-time': backtesttime
    }
    # slack_post(json.dumps(message))
    response = sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/716418748259/quantegy-execute-queue",
            MessageBody=json.dumps(message))
    print(response)
