from parsfonbet import fonbet
from parscloudbet import cloudbet
from parspositive import positive
from parstf import tf
from raybetnew import raybet
from onexline import line1x
from onexlive import live1x
import asyncio
import psycopg2
from config import host, user, password, db_name, port
import time
import schedule
import logging
logger = logging.getLogger(__name__)


# запись данных в бд
def process_data():
    logger.info('[+] process data activated')
    onexlivee = []
    tff = []
    positivee = []
    raybett = []
    onexlinee = []
    try:
        onexlivee = asyncio.run(live1x())
    except Exception as _ex:
        logger.exception('Error in live1x(): %s', _ex)

    try:
        tff = asyncio.run(tf())
    except Exception as _ex:
        logger.exception('Error in tf(): %s', _ex)

    try:
        raybett = asyncio.run(raybet())
    except Exception as _ex:
        logger.exception('Error in raybet(): %s', _ex)

    try:
        positivee = asyncio.run(positive())
    except Exception as _ex:
        logger.exception('Error in positive(): %s', _ex)

    try:
        onexlinee = asyncio.run(line1x())
    except Exception as _ex:
        logger.exception('Error in line1x(): %s', _ex)


    x = cloudbet() + fonbet() + tff + positivee + raybett + onexlinee + onexlivee
    logger.info(f'* {len(x)} - записей')
    global host, user, password, db_name
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS public.pars
                (
                    kof_id serial,
                    status character varying(15),
                    bk_name character varying(15),
                    game_name text,
                    tour_name text,
                    team1 text,
                    team2 text,
                    date_match timestamp(0) without time zone,
                    params text,
                    bet_name text,
                    kofs text,
                    date_request timestamp(0) without time zone
                )
                '''
            )
            for ci in x:

                kof = ' '.join(str(item) for item in ci[9])
                cursor.execute(
                    f"""SELECT kofs from pars where bk_name = '{ci[1]}' and team1 = '{ci[4].replace("'", "''")}' and team2 = '{ci[5].replace("'", "''")}' and date_match = '{ci[6]}' and params = '{ci[7]}' and bet_name = '{ci[8]}'
                    order by date_request desc
                    limit 1"""
                )
                kofs = cursor.fetchone()
                if kofs is not None:
                    if kofs[0] == kof:
                        continue

                cursor.execute(
                    f"""INSERT INTO pars (status, bk_name, game_name, tour_name, team1, team2, date_match, params, bet_name, kofs, date_request) VALUES
                    ('{ci[0]}', '{ci[1]}', '{ci[2]}', '{ci[3].replace("'", "''")}', '{ci[4].replace("'", "''")}', '{ci[5].replace("'", "''")}', '{ci[6]}', '{ci[7]}', '{ci[8]}', '{kof}', '{ci[10]}');"""
                )

            cursor.execute(
                f"""
                UPDATE pars
                SET tour_name = (
                    SELECT COALESCE(
                        (
                        SELECT t2.tour_name
                        FROM pars AS t2
                        WHERE t2.bk_name = 'Fonbet' AND (t2.team1 = pars.team1 AND t2.team2 = pars.team2 OR t2.team1 = pars.team2 AND t2.team2 = pars.team1)
                        AND t2.date_match BETWEEN (pars.date_match - INTERVAL '1 hour') AND (pars.date_match + INTERVAL '1 hour')
                        LIMIT 1
                        ),
                        tour_name
                    )
                    )
                WHERE bk_name <> 'Fonbet';
                """
            )
            logger.info('[-] Data was succesfully inserted')
    except Exception as _ex:
        logger.exception('Error in connection: %s', _ex)
    finally:
        if connection:
            connection.close()
            logger.info('closed')


# удаление ненужных данных с бд
def deletewrite():
    logger.info('deleting lives')
    global host, user, password, db_name,port
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                    SET TIME ZONE 'Europe/Moscow';
                    DELETE FROM pars
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
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting parser')
    schedule.every(2).minutes.do(process_data)
    schedule.every(5).hours.do(deletewrite)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()