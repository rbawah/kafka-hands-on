from kafka import KafkaProducer
import time
import random

from serializer import json_serializer

# connect a producer to the kafka_broker we started in docker
producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = json_serializer,
    acks="all"
    )

message_data = {
    "view": "Clicked to view product",
    "purchase": "Placed order",
    "payment": "Made Payment",
    "delivery": "Order delivered",
    "return": "Requested return"
}

# send 20 test messages
for i in range(20):
    user_id = random.randint(1,10)
    action = random.choice(list(message_data.keys()))
    message = message_data[action]
    value = random.randint(10, 400)

    event = {
        "id": i,
        "user": f"user_{user_id}",
        "action": action,
        "value": value,
        "message": message
    }

    future = producer.send("events-topic", key=event["user"].encode("utf-8"), value=event)

    # block until Kafka acknownledges, the get metadata
    record_metadata = future.get(timeout = 10)

    print(
        f"Produced: {event} "
        f"(Partition: {record_metadata.partition}, Offset: {record_metadata.offset})"
        )
    time.sleep(2)

producer.flush()
producer.close()
