import json
import pymysql
import requests
from datetime import datetime

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
    print(set_dict_from_select(results))
    connection.close()

def get_last_day():
    url = 'https://ssd-api.jpl.nasa.gov/fireball.api?limit=1'

    response = requests.get(url)
    data_json = json.loads(response.text)

    #with open('../test.json', 'w') as file:
    #    json.dump(data_json, file)
    return data_json, response.status_code


def anparse_api_request():
    data, status = get_last_day()
    source = data['signature']
    source = source['source']
    date = dict()
    date['data_request'] = datetime.now().strftime('%Y-%m-%d')
    date['data_requested'] = data['data'][0][0].split()[0]
    count = 1
    return [date, status, source, count]

def insert_data_in_status_request_data(data_request_formated):
    connection = connect_db()
    cursor = connection.cursor()


    sql = f"""
        INSERT INTO nasa_data.status_request_data
        (data_request, data_requested, source, Count_requested_data, status_request)
        VALUES(\'{data_request_formated[0]['data_request']}\',\'{data_request_formated[0]['data_requested']}\', \'{data_request_formated[2]}\', {data_request_formated[3]}, {data_request_formated[1]});
    """
    print(sql)
    cursor.execute(sql)
    connection.commit()

insert_data_in_status_request_data(anparse_api_request())