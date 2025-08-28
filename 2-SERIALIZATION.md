## JSON Serialization

JSON is the most common format for Kafka messages in real-world applications. Using JSON allows you to send structured data (like dictionaries) instead of just plain strings. This is a technical guide for producing and consuming JSON messages with `kafka-python`.

1. Create a new file in your `kafka_project` directory:
```bash
touch serializer.py
```

2. Import `json` and define two functions: `json_serializer` and `json_deserializer`:
```python
import json

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def json_deserializer(data):
    return json.loads(data.decode("utf-8"))
```

3. Make changes to your producer file like below:
```python
from kafka import KafkaProducer
import time

from serializer import json_serializer

# connect a producer to the kafka_broker we started in docker
producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = json_serializer
    )

message_data = [
    "Hello, Kafka",
    "This is my first message",
    "Second message",
    "And yet, another message"
]

# send 5 test messages
for idx, data in enumerate(message_data):
    message = {
        "id": idx,
        "event": "test_event",
        "data": data
    }

    producer.send("test-topic", value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
producer.close()
```

4. Adapt your consumer logic to receive and deserialize the json-structured messages:
```python
from kafka import KafkaConsumer
from serializer import json_deserializer

# start a consumer to subscribe to a topic
consumer = KafkaConsumer(
    "test-topic",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset = "earliest",
    enable_auto_commit = True,
    group_id = "test-topic-group",
    value_deserializer = json_deserializer
)

print("Listening for JSON messages...")

for message in consumer:
    print(f"Received: {message.value["data"]}")
```

