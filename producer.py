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
