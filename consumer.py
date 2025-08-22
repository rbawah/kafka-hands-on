from kafka import KafkaConsumer

# start a consumer to subscribe to a topic
consumer = KafkaConsumer(
    "test-topic",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset = "earliest",
    enable_auto_commit = True,
    group_id = "test-topic-group"
)

print("Listening for message...")

for message in consumer:
    print(f"Received: {message.value.decode()}")
