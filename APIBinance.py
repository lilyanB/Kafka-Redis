import requests
import pandas as pd
from kafka import KafkaProducer
import time


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
    print(data["price"][0])
    return(data)


def pushKafka(giveKey,giveValue):
    producer = KafkaProducer(bootstrap_servers='localhost:29092')
    producer.send('{"payload":{"key":"' + giveKey + '","value":"' + giveValue + '"},' + SCHEMA + '}')
    return True

def all():
    LISTE = listAsset()
    print(LISTE[:48])
    Pair = input("Entrer une paire dans la liste que vous voyez si dessus :")
    temps = float(input("Pendant combien de temps voulez vous envoyer à Kafka le prix? (min)"))
    fin = time.time() + temps * 60 
    while time.time()<fin:
        BIDS = getDepth(Pair,"bids")
        ASKS = getDepth(Pair,"asks")
        MIN = BIDS["price"][0]
        MAX = ASKS["price"][0]
        MOYENNE = (MIN+MAX)/2
        pushKafka("price",MOYENNE)
        pass


if __name__ == '__main__':
    #listAsset()
    #print(getDepth("BTCBUSD","bids"))
    #print(getDepth("BTCBUSD","asks"))
    #pushKafka("employee", "1526")
    all()
    print("END")