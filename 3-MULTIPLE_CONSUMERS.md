



Kafka lets you increase the number of partitions after a topic is created (you can’t decrease).
Run:
```bash
./bin/kafka-topics.sh --alter --topic events-topic --bootstrap-server localhost:9092 --partitions 3
```

Delete the topic:
```bash
./bin/kafka-topics.sh --delete --topic events-topic --bootstrap-server localhost:9092
```

Re-create with 3 partitions:
```bash
./bin/kafka-topics.sh --create --topic events-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

```

To describe the state and details of a specific consumer group:
```bash
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group group1
```