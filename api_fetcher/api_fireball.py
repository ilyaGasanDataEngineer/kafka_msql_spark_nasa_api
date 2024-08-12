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

def get_last_day(start_date:datetime):
    url = f'https://ssd-api.jpl.nasa.gov/fireball.api?date-min={start_date}'

    response = requests.get(url)
    data_json = json.loads(response.text)

    return data_json, response.status_code


def anparse_api_request(start_date:datetime):
    data, status = get_last_day(start_date)
    source = data['signature']
    source = source['source']


    return data['data'], data['signature']['source'], status

def insert_data_in_status_request_data(data_request_formated, source, status):
    connection = connect_db()
    cursor = connection.cursor()
    for i in data_request_formated:
        try:
            sql = f"""
                    INSERT INTO nasa_data.status_request_data
                    (data_request, data_requested, source, Count_requested_data, status_request)
                    VALUES(\'{datetime.now().strftime('%Y-%m-%d')}\',\'{i[0]}\', \'{source}\', {len(data_request_formated)}, {status});
                """
            cursor.execute(sql)
            connection.commit()
        except:
            print('Sorry but data_requested is not unique date: ' + str(i[0]))


#print((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d'))
print(anparse_api_request((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d')))
data_notsorted = anparse_api_request((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d'))
data = data_notsorted[0]
source = data_notsorted[1]
status = data_notsorted[2]

insert_data_in_status_request_data(data, source, status)
#insert_data_in_status_request_data(anparse_api_request())
#print(get_last_day((datetime.now() - relativedelta(months=2)).strftime('%Y-%m-%d')))
#get_data_status_table()
