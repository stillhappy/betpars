import requests
import psycopg2
from config import host, user, password, db_name
from radar import get_game_cloud, get_line_cloud
from datetime import datetime as dt
from datetime import timedelta as td
import time
from datetime import date

now = dt.now()
current_time = now.strftime("%d.%m.%Y %H:%M:%S")
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime((time.strptime(current_time, pattern))))
current_time = now.strftime("%d.%m.%Y %H:%M")
cloud_line = get_line_cloud(epoch, current_time, False)
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        for ci in cloud_line:
            cursor.execute(
                f"""INSERT INTO datakofs (status, bk_name, game_name, tour_name, team1, team2, date_match, params, bet_name, kofs, date_request) VALUES
                ('{ci[0]}', '{ci[1]}', '{ci[2]}', '{ci[3]}', '{ci[4].replace("'", "''")}', '{ci[5].replace("'", "''")}', '{ci[6]}', '{ci[7]}', '{ci[8]}', ARRAY{ci[9]}, '{ci[10]}');"""
            )
        print('Data was succesfully inserted')

except Exception as _ex:
    print('Error', _ex)
finally:
    if connection:
        connection.close()
        print('closed')