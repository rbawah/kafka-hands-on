from kafka import KafkaConsumer
from serializer import json_deserializer
import sys
import time
from kafka.consumer.subscription_state import ConsumerRebalanceListener

group_id = sys.argv[1] if len(sys.argv) > 1 else "default-group"

class RebalanceListener(ConsumerRebalanceListener):
    def on_partitions_assigned(self, assigned):
        print(f"[{group_id}] Assigned partitions: {assigned}")

    def on_partitions_revoked(self, revoked):
        print(f"[{group_id}] Revoked partitions: {revoked}")

# start a consumer to subscribe to a topic
consumer = KafkaConsumer(
    "events-topic",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset = "earliest",
    enable_auto_commit = True,
    group_id = group_id,
    value_deserializer = json_deserializer
)

print(f"Consumer started in group: {group_id}")

# Pass a proper listener instance
consumer.subscribe(["events-topic"], listener=RebalanceListener())

for message in consumer:
    print(f"[{group_id}] Partition: {message.partition}, Offset: {message.offset}, Value: {message.value}")
