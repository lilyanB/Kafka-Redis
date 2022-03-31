import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
PRICE = r.get("price")
print("le prix est de : " + PRICE)