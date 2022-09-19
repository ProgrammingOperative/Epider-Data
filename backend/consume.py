from time import sleep
from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer('new_test_topic',
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer = lambda x: loads(x.decode('utf-8')))

# consumer.subscribe(['new_test_topic']) 

print("Before msg")
for msg in consumer:
    print (msg.value)
    sleep(5)
print("After subscription")
