from flask import Flask, jsonify
from api_fetcher.apod import fetch_apod_data
from api_fetcher.neo import fetch_neo_data
from kafka_producer.producer import create_kafka_producer, send_to_kafka

app = Flask(__name__)

API_KEY = "-----------"  # Замени на свой реальный NASA API ключ

producer = create_kafka_producer()


@app.route('/publish', methods=['GET'])
def publish_data():
    try:
        apod_data = fetch_apod_data(API_KEY)
        neo_data = fetch_neo_data(API_KEY)

        send_to_kafka(producer, 'nasa_apod_topic', apod_data)
        send_to_kafka(producer, 'nasa_neo_topic', neo_data)

        return jsonify({"message": "Data has been published to Kafka"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
