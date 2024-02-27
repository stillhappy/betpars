from parsfonbet import fonbet
from parscloudbet import cloudbet
from parspositive import positive
from parstf import tf
import asyncio
import psycopg2
from config import host, user, password, db_name
import time
import schedule

# запись данных в бд
def process_data():
    x = cloudbet() + fonbet() + asyncio.run(tf()) + asyncio.run(positive())
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
            cursor.execute(
                f"""
                UPDATE datakofs
                SET tour_name = (
                    SELECT COALESCE(
                        (
                        SELECT t2.tour_name
                        FROM datakofs AS t2
                        WHERE t2.bk_name = 'Fonbet' AND (t2.team1 = datakofs.team1 AND t2.team2 = datakofs.team2 OR t2.team1 = datakofs.team2 AND t2.team2 = datakofs.team1)
                        AND t2.date_match BETWEEN (datakofs.date_match - INTERVAL '1 hour') AND (datakofs.date_match + INTERVAL '1 hour')
                        LIMIT 1
                        ),
                        tour_name
                    )
                    )
                WHERE bk_name <> 'Fonbet';
                """
            )

            print('Data was succesfully inserted')
    except Exception as _ex:
        print('Error', _ex)
    finally:
        if connection:
            connection.close()
            print('closed')

# удаление ненужных данных с бд
def deletewrite():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                    DELETE FROM datakofs
                    WHERE date_match <= (CURRENT_TIMESTAMP - INTERVAL '5 hours')
                '''
            )
            print('Data was succesfully deleted')
    except Exception as _ex:
        print('Error', _ex)
    finally:
        if connection:
            connection.close()
            print('closed')

def main():
    schedule.every(2).minutes.do(process_data)
    schedule.every(5).hours.do(process_data)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()