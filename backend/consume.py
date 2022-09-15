from kafka import KafkaConsumer

consumer = KafkaConsumer('example_topic')
for msg in consumer:
    print (msg)