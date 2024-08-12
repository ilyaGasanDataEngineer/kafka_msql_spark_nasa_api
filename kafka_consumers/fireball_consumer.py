from confluent_kafka import Consumer, KafkaException
import pymysql
import json


def create_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'apod_consumer_group',
        'auto.offset.reset': 'earliest'
    })
    return consumer


def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='ilyagasan',
        password='',
        database='nasa_data'
    )
    return connection

def consume_and_store_apod():
    consumer = create_consumer()
    connection = connect_db()
    cursor = connection.cursor()

    consumer.subscribe(['fireball'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            message_value = msg.value()
            if not message_value:
                print("Received empty message")
                continue

            try:
                data = json.loads(message_value.decode('utf-8'))
                print(data)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        connection.close()


if __name__ == "__main__":
    consume_and_store_apod()
