import requests
import pandas as pd
from urllib.parse import urlencode
from kafka import KafkaProducer


URL = 'https://api.binance.com/api/v3/'
PATH = '/order/test'

SCHEMA = '"schema":{"name":"io.github.jaredpetersen.kafkaconnectredis.RedisSetCommand","type":"struct","fields":[{"field":"key","type":"string","optional":false},{"field":"value","type":"string","optional":false},{"field":"expiration","type":"struct","fields":[{"field":"type","type":"string","optional":false},{"field":"time","type":"int64","optional":true}],"optional":true},{"field":"condition","type":"string","optional":true}]}'


def listAsset():
    r = requests.get(URL + "exchangeInfo")
    results = r.json()
    ListAss = []
    for s in results['symbols']:
        ListAss.append(s['symbol'])
    return ListAss


def getDepth(SYMBOLE,INFO):
  r = requests.get(URL + "depth", params=dict(symbol=SYMBOLE))
  results = r.json()
  frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"], dtype=float) for side in [INFO]}
  frames_list = [frames[side].assign(side=side) for side in frames]
  data = pd.concat(frames_list, axis="index", ignore_index=True, sort=True)
  return(data)


def pushKafka(giveKey,giveValue):
    producer = KafkaProducer(bootstrap_servers='localhost:29092')
    producer.send('{"payload":{"key":"' + giveKey + '","value":"' + giveValue + '"},' + SCHEMA + '}')
    return True

def all():
    LISTE = listAsset()
    FirstList = LISTE[0]
    BIDS = getDepth(FirstList,"bids")
    ASKS = getDepth(FirstList,"asks")
    listBIDS = []
    listASKS = []
    for i in range(1,len(BIDS)):
        valuee = BIDS["price"][i]
        listBIDS.append(valuee)
        #print(listBIDS)
        pushKafka("price" + i,valuee)
    for i in range(1, len(ASKS)):
        valuee = ASKS["price"][i]
        listASKS.append(valuee)
        #print(listASKS)
        pushKafka("price" + i,valuee)


if __name__ == '__main__':
    #listAsset()
    #print(getDepth("BTCBUSD","bids"))
    #print(getDepth("BTCBUSD","asks"))
    #pushKafka("employee", "1526")
    all()