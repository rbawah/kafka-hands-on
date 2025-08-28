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
