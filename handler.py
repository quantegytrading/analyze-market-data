# handler.py
import json
import boto3

from domain.objects import Candle, ThreeCandles
from analysis import bullish_patterns_present, bearish_patterns_present


def main(event, context):
    sns = boto3.client('sns')
    # dynamodb = boto3.resource('dynamodb')
    buys = []
    sells = []
    message = {}
    event_message = event['Records'][0]['Sns']['Message']
    market_data = event_message['market_data']
    # symbols_string = event_message['currencies']
    # symbols_string = symbols_string.lstrip('[')
    # symbols_string = symbols_string.rstrip(']')
    # symbols_string = symbols_string.replace('"', '')
    # symbols_string.replace(" ", "")
    # symbols = symbols_string.split(",")
    # keys = []
    # for symbol in symbols:
    #     sym_dic = {"symbol": symbol.strip()}
    #     keys.append(sym_dic)
    # keys_dict = {"Keys": keys}
    # responses = dynamodb.batch_get_item(
    #     RequestItems={
    #         'market-data': keys_dict
    #     })
    # market_data: list = responses['Responses']["market-data"]
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
