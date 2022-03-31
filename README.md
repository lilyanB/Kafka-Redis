# Kafka-Redis

Designing Distributed Systems 2022
use of Kafka and Docker compose

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
With this files, you will push the Bitcoin price during the time you want.

Verify you are all requirements.
```python
import requests
import pandas as pd
from kafka import KafkaProducer
import kafka
```

### Run Affiche.py
When you want to have the Price, you can run this files

Verify you are all requirements.
```python
import redis
```