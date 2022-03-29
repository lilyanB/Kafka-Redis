import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
PRICE=[]
for i in range(1,5):
    price = r.get("price" + i)
    PRICE.append(price)
print("le prix est de : " + PRICE)
