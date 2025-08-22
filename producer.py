from kafka import KafkaProducer
import time

# connect a producer to the kafka_broker we started in docker
producer = KafkaProducer(bootstrap_servers = "localhost:9092")

messages = [
    "Hello, Kafka",
    "This is my first message",
    "This is my second message",
    "and yet, another message"
]

# send 5 test messages
for message in messages:
    message = f"{message}".encode("utf-8")
    producer.send("test-topic", message)
    print(f"Sent: {message.decode()}")
    time.sleep(1)

producer.flush()
producer.close()
