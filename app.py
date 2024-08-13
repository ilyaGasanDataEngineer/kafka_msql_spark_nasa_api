from flask import Flask, jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

from api_fetcher.apod import fetch_apod_data
from api_fetcher.neo import fetch_neo_data
from kafka_producer.producer import create_kafka_producer, send_to_kafka
from kafka_consumers.api_fireball import anparse_api_request

app = Flask(__name__)

API_KEY = "vcFXjzqTyPsfsakIecpecUCXroFTMH4uXawhalU8"  # Замени на свой реальный NASA API ключ

producer = create_kafka_producer()


def convert_to_json(data):
    headers = [
        "datetime", "energy", "impact_e", "velocity", "direction",
        "latitude", "longitude", "altitude", "impact_altitude"
    ]

    records, source, status_code = data

    json_data = []
    for record in records:
        record_dict = {}
        for i, value in enumerate(record):
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except (ValueError, TypeError):
                pass

            if i == 0:
                try:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass

            record_dict[headers[i]] = value
        json_data.append(record_dict)

    result = {
        "source": source,
        "status_code": status_code,
        "records": json_data
    }

    # Конвертируем в JSON
    return json.dumps(result, indent=4, default=str)

@app.route('/publish', methods=['GET'])
def publish_data():
    try:
        apod_data = fetch_apod_data(API_KEY)
        neo_data = fetch_neo_data(API_KEY)

        send_to_kafka(producer, 'nasa_apod_topic', apod_data)
        send_to_kafka(producer, 'nasa_neo_topic', neo_data)
        print(type(neo_data))
        return jsonify({"message": "Data has been published to Kafka"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nasa_fireball')
def publish_data_fireball():
    try:
        fireball_data = anparse_api_request((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d'))
        send_to_kafka(producer, 'fireball', convert_to_json(fireball_data))

        print(fireball_data)
        return convert_to_json(fireball_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
