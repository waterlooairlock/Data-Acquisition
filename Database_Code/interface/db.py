import os
import MySQLdb
import time
import datetime

import json

_connection = None


def get_connection():
    global _connection
    if not _connection:
        config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
        settings = json.load(open(config_file_path)).get('database')
        _connection = db = MySQLdb.connect(
            host=settings.get('host'), user=settings.get('user'), passwd=settings.get('passwrd'), db=settings.get('db'))
    return _connection

def add_temp_reading(sensor_id, reading):
    connection = get_connection()
    cur = connection.cursor()
    ts = time.time()
    timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    sql_insert_query = "INSERT INTO temp_readings (sensor_id, sensor_reading, time) VALUES (%s,%s,%s)"
    cur.execute(sql_insert_query, (sensor_id, reading, timestamp_str))

def get_latest_temp_readings():
    connection = get_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT * FROM temp_readings WHERE (id) IN (
        SELECT max(id) FROM temp_readings GROUP BY sensor_id
    )''')
    return cur.fetchall()

__all__ = ['add_temp_reading', 'get_latest_temp_readings']