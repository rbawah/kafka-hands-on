# Consumer Groups: Multiple Consumers and Producers

This stage demonstrates how Kafka producers and consumers work together with consumer groups and partitioning. You’ll see how Kafka balances load across multiple consumers, how to inspect and manage consumer groups, and how to control message distribution using keys.

The examples include:

- Create and manage topics – including adding partitions and deleting/re-creating topics.

- Run producers and consumers – see how messages get distributed across partitions.

- Work with consumer groups – understand how Kafka assigns partitions to consumers in the same group.

- Control partitioning with keys – send messages to specific partitions or let Kafka decide.

- Apply best practices – choose keys that balance load and maintain ordering guarantees.

## Some useful commands

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

# Best practices for choosing keys in Kafka

🔑 1. Use keys that matter for ordering

Kafka guarantees ordering only within a partition.
If your application needs all events for a single user to be processed in order → use user_id as the key.

Example:

"user_123" → all messages for that user always land in the same partition.

This ensures correct order for clickstream, shopping carts, payments, etc.

⚖️ 2. Balance across partitions

If you always use the same key (e.g., "user_1"), all messages go to one partition → bottleneck.
Better: pick a key that has enough variety to spread load, e.g. "user_id", "device_id", "order_id".

The more unique keys, the better Kafka’s hash will spread events across partitions.

🧩 3. When to use null key

If ordering per entity doesn’t matter, you can send messages with key=None.
Kafka then distributes events across partitions (round-robin).

Example: metrics, logs, IoT sensor events where strict per-entity ordering is not critical.

🔄 4. Consistency across producers

If multiple producers send to the same topic, they must use the same keying strategy.
Otherwise, you risk splitting one entity’s events across different partitions (breaking ordering).

📈 5. Think ahead for scaling

Partition count is fixed when the topic is created.
If you’ll scale later (e.g., from 3 → 12 partitions), pick a key that works well with different partition counts.

Example: hashing on user_id scales better than hashing on country (since some countries dominate).

