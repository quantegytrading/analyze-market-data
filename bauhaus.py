# apolloniabak.py
import json
import boto3

from domain.objects import Candle, ThreeCandles
from analyze import bullish_patterns_present, bearish_patterns_present


def get_candle_package(symbol, candles):
    c3 = candles[0]
    c2 = candles[1]
    c1 = candles[2]
    candle3 = Candle(c3[0], symbol, c3[1], c3[2], c3[3], c3[4], c3[0])
    candle2 = Candle(c2[0], symbol, c2[1], c2[2], c2[3], c2[4], c2[0])
    candle1 = Candle(c1[0], symbol, c1[1], c1[2], c1[3], c1[4], c1[0])
    return ThreeCandles(candle1, candle2, candle3)


def get_env(recv_topic_arn: str) -> str:
    if recv_topic_arn.find("backtest") != -1:
        return "backtest"
    else:
        return "soak"


def get_target_arn(recv_topic_arn: str) -> str:
    if recv_topic_arn.find("backtest") != -1:
        return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-backtest"
    else:
        return "arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-soak"


def bauhaus(ccc):
    buys = []
    symbol = ""
    # if bullish_patterns_present(ccc):
    if bearish_patterns_present(ccc):
        symbol = ccc.candle1.s
        buys.append(symbol)
    return buys


def main(event, context):

    algorithm = "bauhaus"

    sns = boto3.client('sns')
    buys = []
    buy_prices = {}
    sells = []
    message = {}
    event_message = json.loads(event['Records'][0]['Sns']['Message'])
    recv_topic_arn = event['Records'][0]['Sns']['TopicArn']
    env = get_env(recv_topic_arn)
    data_type = event_message['data_type']
    exchange = event_message['exchange']
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
            buys = bauhaus(ccc)
            buy_prices[symbol] = ccc.candle1.c

    print("Buys: " + str(buys))
    print("Sells: " + str(sells))

    message['buys'] = buys
    message['buy_prices'] = buy_prices
    message['sells'] = sells
    message['algorithm'] = algorithm
    message['data_type'] = data_type
    message['exchange'] = exchange
    message['backtest-time'] = backtesttime
    message['env'] = env
    target_arn = get_target_arn(recv_topic_arn)
    print(env)
    print(target_arn)

    sns.publish(
        TargetArn=target_arn,
        Message=json.dumps(message)
    )


if __name__ == "__main__":
    main('', '')
