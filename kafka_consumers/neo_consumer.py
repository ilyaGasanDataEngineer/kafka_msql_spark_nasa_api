from confluent_kafka import Consumer, KafkaException
import pymysql
import json


def create_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'neo_consumer_group',
        'auto.offset.reset': 'earliest'
    })
    return consumer


def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='nasa_data'
    )
    return connection


def consume_and_store_neo():
    consumer = create_consumer()
    connection = connect_db()
    cursor = connection.cursor()

    consumer.subscribe(['nasa_neo_topic'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            data = json.loads(msg.value().decode('utf-8'))
            neo_objects = data.get('near_earth_objects', [])

            for date, objects in neo_objects.items():
                for obj in objects:
                    sql = """INSERT INTO neo (name, close_approach_date, estimated_diameter_min_km, 
                                              estimated_diameter_max_km, velocity_km_per_hour, miss_distance_km)
                             VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (
                        obj.get('name'),
                        date,
                        obj['estimated_diameter']['kilometers']['estimated_diameter_min'],
                        obj['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                        obj['close_approach_data'][0]['miss_distance']['kilometers']
                    ))
            connection.commit()

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        connection.close()


if __name__ == "__main__":
    consume_and_store_neo()
