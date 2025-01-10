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


# def get_env(recv_topic_arn: str) -> str:
#     if recv_topic_arn.find("backtest") != -1:
#         return "backtest"
#     else:
#         return "soak"
#
#
# def get_target_arn(recv_topic_arn: str, prod: str) -> str:
#     print("Prod: " + prod)
#     if prod == "true":
#         return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-prod"
#     elif recv_topic_arn.find("backtest") != -1:
#         return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-backtest"
#     else:
#         return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-soak"


# def slack_post(msg: str):
#     client = WebClient(token=os.environ['SLACK_TOKEN'])
#     client.chat_postMessage(channel=f"#quantegy-crypto", text=msg, icon_emoji=':moneybag:', username='Quantegy')


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
        'prices': buy_prices,
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