# Kafka-Redis

Lilyan BASTIEN 2022

### Usage of the scripts
```bash
cd Kafka-Redis
```

### Setup all Docker containers
```bash
docker-compose up
```

### Install the Redis Kafa Connect connector from HTTP command
```bash
curl -s -X POST -H 'Content-Type: application/json' --data @redis-sink-config.json http://localhost:8083/connectors
```
### Run APIBinance.py
With this files, you will push the Bitcoin price during 5min
You can change "time" depending on your needs

### Run Affiche.py
When you want to have the Price, you can run this files