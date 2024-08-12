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

def insert_data_in_status_request_data(data_request_formated, source, status):
    connection = connect_db()
    cursor = connection.cursor()
    #print(f'{data_request_formated} \n[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[')

    for i in data_request_formated:
        try:
            sql = """
                    INSERT INTO nasa_data.status_request_data
                    (data_request, data_requested, source, Count_requested_data, status_request)
                    VALUES (%s, %s, %s, %s, %s)
                """
            values = (
                datetime.now().strftime('%Y-%m-%d'),
                i[0],
                source,
                len(data_request_formated),
                status
            )
            cursor.execute(sql, values)

            last_id = cursor.lastrowid

            print(f"Inserted record ID: {last_id} date's id: {i[0]}")
            sql = """
                    INSERT INTO nasa_data.data_nasa
                    (id_request, energy, impact_e, lat, lat_dir, lon, lon_dir, alt, vel)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            print(f'{i}   dddddddddddddddddddddddddddddddddddddddddd')

            values = (
                last_id,
                i[1],
                i[2],
                i[3],
                i[4],
                i[5],
                i[6],
                i[7],
                i[8]
            )
            cursor.execute(sql, values)

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            date_value = datetime.strptime(i[0].split()[0], "%Y-%m-%d").date()
            print(f'Sorry but data_requested is not unique date: {i[0]}')

            sql = """
                    SELECT id FROM nasa_data.status_request_data
                    WHERE data_requested = %s
                """
            cursor.execute(sql, (date_value,))
            result = cursor.fetchone()

            if result:
                last_id = result[0]
                print(f"Existing record ID: {last_id}")

    connection.commit()

    cursor.close()
    connection.close()



data_notsorted = anparse_api_request((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d'))
data = data_notsorted[0]
source = data_notsorted[1]
status = data_notsorted[2]
insert_data_in_status_request_data(data, source, status)

#print(get_data((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d'))[0]['data'][0])
