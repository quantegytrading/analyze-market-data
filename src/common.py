# apolloniabak.py
import json
import os

import boto3
from src.domain.objects import Candle, ThreeCandles


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


def get_env(recv_topic_arn: str) -> str:
    if recv_topic_arn.find("backtest") != -1:
        return "backtest"
    else:
        return "soak"


def get_target_arn(recv_topic_arn: str, prod: str) -> str:
    print("Prod: " + prod)
    if prod == "true":
        return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-prod"
    elif recv_topic_arn.find("backtest") != -1:
        return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-backtest"
    else:
        return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-soak"


def go(event, algorithm, algorithm_fn):
    sns = boto3.client('sns')
    buys = []
    buy_prices = {}
    sells = []
    event_message = json.loads(event['Records'][0]['Sns']['Message'])
    recv_topic_arn = event['Records'][0]['Sns']['TopicArn']
    env = get_env(recv_topic_arn)
    data_type = event_message['data_type']
    exchange = event_message['exchange']
    interval = event_message['interval']
    market_data_list = event_message['market_data']
    backtesttime = ""

    for market_data in market_data_list:
        symbol = market_data['symbol']
        data = json.loads(market_data['data'])
        if len(data) == 0:
            print("No data found for symbol: " + str(symbol))
        else:
            last_candles = data[-3:]
            ccc = get_candle_package(symbol, last_candles)
            backtesttime = ccc.candle1.u
            bs = algorithm_fn(symbol, data)
            buys.append(bs.buys)
            sells.append(bs.sells)
            buy_prices[symbol] = ccc.candle1.c

    flat_buys = []
    for buy in buys:
        if buy:
            flat_buys.append(buy[0])

    flat_sells = []
    for sell in sells:
        if sell:
            flat_sells.append(sell[0])

    message = {
        'algorithm': algorithm,
        'env': env,
        'interval': interval,
        'buys': flat_buys,
        'buy_prices': buy_prices,
        'sells': flat_sells,
        'data_type': data_type,
        'exchange': exchange,
        'backtest-time': backtesttime
    }

    target_arn = get_target_arn(recv_topic_arn, os.environ['prod'])

    sns.publish(
        TargetArn=target_arn,
        Message=json.dumps(message)
    )