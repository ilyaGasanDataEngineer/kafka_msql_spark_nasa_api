import json
import pymysql
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# key =

def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='ilyagasan',
        password='',
        database='nasa_data'
    )
    return connection

def set_dict_from_select(data:tuple)->dict:
    data_in_status = dict()
    for row in data:
        data_in_status[f'{row[0]}'] = row[1]
    return data_in_status

def get_data_status_table():
    connection = connect_db()
    cursor = connection.cursor()

    sql = """
        SELECT * FROM status_request_data
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    #print(results[0])
    connection.close()

def get_data(start_date:datetime):
    url = f'https://ssd-api.jpl.nasa.gov/fireball.api?date-min={start_date}'

    response = requests.get(url)
    data_json = json.loads(response.text)

    return data_json, response.status_code


def anparse_api_request(start_date:datetime):
    data, status = get_data(start_date)
    source = data['signature']
    source = source['source']


    return data['data'], data['signature']['source'], status


def insert_data_in_status_request_data(data_dict):
    connection = connect_db()
    cursor = connection.cursor()

    print(data_dict)
    for data in data_dict['records']:
        print(data)
        try:
            sql_query = """
                INSERT INTO nasa_data.status_request_data
                (data_request, data_requested, source, Count_requested_data, status_request)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                id = LAST_INSERT_ID(id);
            """
            values = (
                datetime.now().strftime('%Y-%m-%d'),
                data['datetime'],
                data_dict['source'],
                len(data_dict['records']),
                data_dict['status_code']
            )

            cursor.execute(sql_query, values)
            last_id = cursor.lastrowid

            sql_query = """
                INSERT INTO nasa_data.data_nasa
                (id_request, energy, impact_e, lat, lat_dir, lon, lon_dir, alt, vel)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (
                last_id,
                data['energy'],
                data['impact_e'],
                data['latitude'],
                data['direction'],
                data['latitude'],
                data['longitude'],
                data['altitude'],
                data['velocity']
            )
            cursor.execute(sql_query, values)

        except pymysql.err.IntegrityError as e:
            if "Duplicate entry" in str(e):
                print(f"Duplicate entry found, skipping: {e}")
                connection.rollback()
                continue
            else:
                print(f"Integrity error occurred: {e}")
                connection.rollback()
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
            continue

    connection.commit()
    cursor.close()
    connection.close()
