import requests
import psycopg2
from config import host, user, password, db_name
from radar import get_line_cloud, get_value_fonbet, fonbet_live, fonbet_line
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
cloud_live = get_line_cloud(epoch, current_time, True)
fon_line = get_value_fonbet(fonbet_line())
fon_live = get_value_fonbet(fonbet_live())
x = cloud_line + cloud_live + fon_line + fon_live
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True


    with connection.cursor() as cursor:
        for ci in x:
            cursor.execute(
                f"""SELECT kofs from datakofs where bk_name = '{ci[1]}' and team1 = '{ci[4].replace("'", "''")}' and team2 = '{ci[5].replace("'", "''")}' and params = '{ci[7]}' and bet_name = '{ci[8]}'
                order by date_request desc
                limit 1"""
            )
            kofs = cursor.fetchone()
            if kofs is not None:
                if kofs[0] == ci[9]:
                    continue
            print(kofs)
            print(ci[9], 'data')
            cursor.execute(
                f"""INSERT INTO datakofs (status, bk_name, game_name, tour_name, team1, team2, date_match, params, bet_name, kofs, date_request) VALUES
                ('{ci[0]}', '{ci[1]}', '{ci[2]}', '{ci[3].replace("'", "''")}', '{ci[4].replace("'", "''")}', '{ci[5].replace("'", "''")}', '{ci[6]}', '{ci[7]}', '{ci[8]}', ARRAY{ci[9]}, '{ci[10]}');"""
            )


        print('Data was succesfully inserted')
except Exception as _ex:
    print('Error', _ex)
finally:
    if connection:
        connection.close()
        print('closed')

