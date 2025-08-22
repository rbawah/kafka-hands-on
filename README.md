## Kafka - Getting Started
### Kafka on the Console
There are [several ways](https://kafka.apache.org/quickstart) to install **Kafka**. For the purpose of this course, we will use a **JVM Based Apache Kafka Docker Image**.
1. Pull the docker image (for guaranted stability let's pull version `4.0.0` instead of `latest`):
```bash
docker pull apache/kafka:4.0.0
```
2. Start the Kafka docker container:
```bash
docker run --name kafka_broker -p 9092:9092 apache/kafka:4.0.0
```
This will run the container in attached mode with the name `kafka_broker` on port `9092`. Now open a new terminal to continue.
3. In a new terminal, open a shell in the broker container:

```bash
docker exec --workdir /opt/kafka/ -it kafka_broker sh
```

4. Check for the list of available topics. Should be empty since we have not created any topics yet:
```bash
./bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```
5. Create a topic called `test-topic`:
```bash
./bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic
```
if we check our list of topics again, we should see `test-topic` listed.

6. Open the console producer (to publish messages to `test-topic`) that ships with Kafka and write 2 events to `test-topic`:
```bash
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test-topic
```
Then you can type your messages after the `>`, and press `Enter/Return`:
```bash
> hello world
> this is my very first message
> this is my second message
```
7. Open another terminal to start the console consumer that reads messages from the topic `test-topic`:
```bash
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```
By adding the flag `--from-beginning`, the consumer will read all messages (old and new). without the flag, the consumer will only read messages that came after it was started. 
- Remember: You have to open a shell in our `kafka_broker` docker container, as we did in step 3, before trying to start the consumer.

You should see all the messages printed on the console. 
You can send new messages from the producer and check for them in the console consumer.

NOTE: To close the console consumer/producer, press `CTRL + C` or `CTRL + Z` to return to the docker shell. You can then exit to your main shell by running the command `exit`. You might have to run it twice.

NOTE: Keep your `kafka_broker` container running to try the python set up below.

%md
### The Python Client

1. In your home directory, make a folder called `kafka_projects`: `mkdir ~/kafka_project`
`cd ~/kafka_project`

Create a virtual environment prevent conflicts between projects. Use the Python-built `venv`:
```bash
python3 -m venv .venv
```
You can name it differently, but `.venv` is conventional.

2. Activate the virtual environment: 
```bash
source ~/kafka_project/.venv/bin/activate
```

3. Upgrade `pip`. Always good to start afresh:
```bash
pip install --upgrade pip
```

4. Install `kafka-python` and other optional packages:
```bash
pip install kafka-python 'kafka-python[crc32c]' 
```
Why do we want `'kafka-python[crc32c]'`?

Kafka uses `CRC32C` checksums to validate message integrity. With it, checksum validation is done in C (much faster). Without this, `kafka-python` falls back to a pure Python implementation, which is slower. Highly recommended if you’re consuming/producing lots of messages.

5. Set up `Producer`
create a file `producer.py`: `touch ~/kafka_project/producer.py`

```python
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
```

6. Set up a `Consumer`, create file `consumer.py`: `touch ~/kafka_project/consumer.py`
```python
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

```
7. Execute the producer file: `python producer.py` and the consumer file `python consumer.py` in separate terminals with the virtual environment activated.

