from confluent_kafka import Producer
import json

def create_kafka_producer():
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    return producer

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send_to_kafka(producer, topic, data):
    producer.produce(topic, value=json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()
