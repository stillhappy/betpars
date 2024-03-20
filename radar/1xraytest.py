import psycopg2
import time
import schedule
from parsfonbet import fonbet
from raybet import raybet
from parsraybetlive import raybetl
from onexline import line1x
from onexlive import live1x
import asyncio
import json
import requests
print('[*] py activated')

onexlivee = []
raybett = []
raybetll = []
onexlinee = []
try:
    onexlivee = asyncio.run(live1x())
except Exception as _ex:
    print('Error', _ex)
try:
    raybett = asyncio.run(raybet())
except Exception as _ex:
    print('Error', _ex)
try:
    raybetll = asyncio.run(raybetl())
except Exception as _ex:
    print('Error', _ex)
try:
    onexlinee = asyncio.run(line1x())
except Exception as _ex:
    print('Error', _ex)
x = onexlinee + onexlivee + raybett + raybetll
# запись данных в бд
def process_data():
    print('[+] process data activated')
    host = '127.0.0.1'
    user = 'postgres'
    password = '12345'
    db_name = 'betparser'
    x = fonbet()
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        print(' '.join(x[0][9]))
        with connection.cursor() as cursor:
            for ci in x:
                kof = ' '.join(ci[9])
                print(kof)
                cursor.execute(
                    f"""SELECT kofs from datakofs where bk_name = '{ci[1]}' and team1 = '{ci[4].replace("'", "''")}' and team2 = '{ci[5].replace("'", "''")}' and params = '{ci[7]}' and bet_name = '{ci[8]}'
                                    order by date_request desc
                                    limit 1"""
                )
                kofs = cursor.fetchone()
                if kofs is not None:
                    print(kofs)
                    if kofs[0] == kof:
                        continue
                cursor.execute(
                    f"""INSERT INTO datakofs (status, bk_name, game_name, tour_name, team1, team2, date_match, params, bet_name, kofs, date_request) VALUES
                                    ('{ci[0]}', '{ci[1]}', '{ci[2]}', '{ci[3].replace("'", "''")}', '{ci[4].replace("'", "''")}', '{ci[5].replace("'", "''")}', '{ci[6]}', '{ci[7]}', '{ci[8]}', '{kof}', '{ci[10]}');"""
                )


    except Exception as _ex:
        print('Error', _ex)
    finally:
        if connection:
            connection.close()
            print('closed')


print(*x, sep='\n')

