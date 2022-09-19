import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from json import dumps



# from json import dumps

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer = lambda x:dumps(x).encode('utf-8')) 
data = {'message': 'Hey Titus v3'}
publish = producer.send('new_test_topic', data)

try:
    record_metadata = publish.get(timeout = 30)
except KafkaError:
    logging.exception("Delivery Failed!")
    pass

#Successful publish returns topic and offset
print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)
