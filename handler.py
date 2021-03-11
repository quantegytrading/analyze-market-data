# handler.py
import json
import boto3

from domain.objects import Candle, ThreeCandles
from analysis import bullish_patterns_present, bearish_patterns_present


def get_candle_package(symbol, candles):
    c3 = candles[0]
    c2 = candles[1]
    c1 = candles[2]
    candle3 = Candle(c3[0], symbol, c3[1], c3[2], c3[3], c3[4], c3[0])
    candle2 = Candle(c2[0], symbol, c2[1], c2[2], c2[3], c2[4], c2[0])
    candle1 = Candle(c1[0], symbol, c1[1], c1[2], c1[3], c1[4], c1[0])
    return ThreeCandles(candle1, candle2, candle3)


def main(event, context):
    sns = boto3.client('sns')
    buys = []
    sells = []
    message = {}

    event_message = json.loads(event['Records'][0]['Sns']['Message'])

    data_type = event_message['data_type']
    exchange = event_message['exchange']
    market_data_list = event_message['market_data']

    for market_data in market_data_list:
        symbol = market_data['symbol']
        data = json.loads(market_data['data'])
        if len(data) == 0:
            print("No data found for symbol: " + str(symbol))
        else:
            last_candles = data[-3:]
            ccc = get_candle_package(symbol, last_candles)
            if bullish_patterns_present(ccc):
                buys.append(symbol)
            if bearish_patterns_present(ccc):
                sells.append(symbol)

    print("Buys: " + str(buys))
    print("Sells: " + str(sells))
    sns.publish(
        TargetArn='arn:aws:sns:us-east-1:716418748259:trade-quantegy-data-soak',
        Message=json.dumps(message)
    )


if __name__ == "__main__":
    main('', '')
