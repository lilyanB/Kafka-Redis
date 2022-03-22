import requests
import pandas as pd
from urllib.parse import urlencode
from kafka import KafkaProducer


URL = 'https://api.binance.com/api/v3/'
PATH = '/order/test'

""" "payload":{"key":"users:1:username","value":"Greg"}, """
SCHEMA = '"schema":{"name":"io.github.jaredpetersen.kafkaconnectredis.RedisSetCommand","type":"struct","fields":[{"field":"key","type":"string","optional":false},{"field":"value","type":"string","optional":false},{"field":"expiration","type":"struct","fields":[{"field":"type","type":"string","optional":false},{"field":"time","type":"int64","optional":true}],"optional":true},{"field":"condition","type":"string","optional":true}]}'


def listAsset():
    r = requests.get(URL + "exchangeInfo")
    results = r.json()
    for s in results['symbols']:
        print(s['symbol'])


def getDepth(SYMBOLE,INFO):
  r = requests.get(URL + "depth", params=dict(symbol=SYMBOLE))
  results = r.json()
  frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"], dtype=float) for side in [INFO]}
  return(frames)


def pushKafka(giveKey,giveValue):
    producer = KafkaProducer(bootstrap_servers='localhost:29092')
    for _ in range(2):
        producer.send('{"payload":{"key":"' + giveKey + '","value":"' + giveValue + '"},' + SCHEMA + '}')

    return True


if __name__ == '__main__':
    print(listAsset())
    print(getDepth("BTCBUSD","bids"))
    print(getDepth("BTCBUSD","asks"))
    pushKafka("employee", "1526")