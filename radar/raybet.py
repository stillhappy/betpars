from datetime import datetime
from datetime import timedelta
import asyncio
import aiohttp
import itertools
import json
from filtertour import filterteam, filtertourn
from random import choice

def get_coef(game_result):
    bet_list_final = []
    game_name = {'DOTA2': 'Dota 2', 'CS2': 'Counter-Strike', '无畏契约': 'Valorant', '英雄联盟': 'LoL'}
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    date_format = '%Y-%m-%d %H:%M'
    initial_date = datetime.strptime(current_time, date_format)
    updated_date = initial_date + timedelta(hours=3)
    current_time = updated_date.strftime(date_format)
    for item in game_result:
        kefs = []
        for i in range(len(item['result']['odds'])):
            if item['result']['odds'][i]['group_short_name'] == 'Winner':
                kefs.append(item['result']['odds'][i]['odds'])
                kefs.append(item['result']['odds'][i]['name'])
        if len(kefs) > 0:
            time = datetime.strptime(item['result']['start_time'], "%Y-%m-%d %H:%M:%S") - timedelta(
                hours=5, )
            time = time.strftime('%Y-%m-%d %H:%M')
            if time > current_time:

                time = datetime.strptime(item['result']['start_time'], "%Y-%m-%d %H:%M:%S") - timedelta(
                    hours=5, )
                time = time.strftime('%Y-%m-%d %H:%M')
                if time > current_time:
                    bet_list = []
                    bet_list.append('line')
                    bet_list.append('raybet')
                    game_check = item['result']['game_name']
                    if game_check in game_name:
                        game_check = game_name[game_check]
                    bet_list.append(game_check)
                    bet_list.append(item['result']['tournament_short_name'])
                    team1 = item['result']['team'][0]['team_name'].rstrip().lower().title().replace('Club', '').replace(
                        'Team', '').replace(
                        'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                                   ' ').replace(
                        'Challengers', '').replace('Chall', '').strip()
                    team2 = item['result']['team'][1]['team_name'].rstrip().lower().title().replace('Club', '').replace(
                        'Team', '').replace(
                        'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                                   ' ').replace(
                        'Challengers', '').replace('Chall', '').strip()
                    bet_list.append(filterteam.get(team1, team1))
                    bet_list.append(filterteam.get(team2, team2))
                    bet_list.append(time)
                    bet_list_copy = bet_list.copy()
                    if item['result']['round'] == 'bo2':
                        bet_list.append('1-я карта')
                    else:
                        bet_list.append('Общая')
                    bet_list.append('Исходы')
                    if kefs[1].startswith(bet_list[4]):
                        kefs_event = [kefs[0], kefs[2]]
                        bet_list.append(kefs_event)
                    else:
                        kefs_event = [kefs[2], kefs[0]]
                        bet_list.append(kefs_event)
                    bet_list.append(current_time)
                    if len(bet_list) > 0:
                        bet_list_final.append(bet_list)

                    if len(kefs) > 4:
                        bet_list = bet_list_copy.copy()
                        if item['result']['round'] == 'bo2':
                            bet_list.append('2-я карта')
                        else:
                            bet_list.append('1-я карта')

                        bet_list.append('Исходы')
                        if kefs[5].startswith(bet_list[4]):
                            kefs_event = [kefs[4], kefs[6]]
                            bet_list.append(kefs_event)
                        else:
                            kefs_event = [kefs[6], kefs[4]]
                            bet_list.append(kefs_event)

                        bet_list.append(current_time)
                        if len(bet_list) > 0:
                            bet_list_final.append(bet_list)
                    if len(kefs) > 8:
                        bet_list = bet_list_copy.copy()
                        bet_list.append('2-я карта')
                        bet_list.append('Исходы')
                        if kefs[9].startswith(bet_list[4]):
                            kefs_event = [kefs[8], kefs[10]]
                            bet_list.append(kefs_event)
                        else:
                            kefs_event = [kefs[10], kefs[8]]
                            bet_list.append(kefs_event)
                        bet_list.append(current_time)
                        if len(bet_list) > 0:
                         bet_list_final.append(bet_list)
                    kefs = []
                    for i in range(len(item['result']['odds'])):
                        if item['result']['odds'][i]['group_short_name'] == 'Round Handicap':
                            kefs.append(item['result']['odds'][i]['odds'])
                            kefs.append(item['result']['odds'][i]['name'])
                    if len(kefs) > 0:
                        bet_fora = bet_list_copy.copy()
                        bet_fora.append('1-я карта')
                        if kefs[1].startswith(bet_fora[4]):
                            bet_fora.append('Фора 1 (' + str(kefs[1])[-4:] + ')')
                            kefs_fora = [kefs[0], kefs[2]]
                            bet_fora.append(kefs_fora)
                        else:
                            bet_fora.append('Фора 1 ('+ str(kefs[3])[-4:] + ')')
                            kefs_fora = [kefs[2], kefs[0]]
                            bet_fora.append(kefs_fora)
                        bet_fora.append(current_time)
                        if len(bet_fora) > 0:
                            bet_list_final.append(bet_fora)
                    if len(kefs) > 4:
                        bet_fora = bet_list_copy.copy()
                        bet_fora.append('2-я карта')
                        if kefs[5].startswith(bet_fora[4]):
                            bet_fora.append('Фора 1 ('+ str(kefs[5])[-4:] + ')')
                            kefs_fora = [kefs[4], kefs[6]]
                            bet_fora.append(kefs_fora)
                        else:
                            bet_fora.append('Фора 1 (' + str(kefs[7])[-4:] + ')')
                            kefs_fora = [kefs[6], kefs[4]]
                            bet_fora.append(kefs_fora)
                        bet_fora.append(current_time)
                        if len(bet_fora) > 0:
                            bet_list_final.append(bet_fora)
                        kefs = []
                        for i in range(len(item['result']['odds'])):

                            if item['result']['odds'][i]['group_short_name'] == 'Total Rounds' and (item['result']['odds'][i]['value'] != 'odd' or item['result']['odds'][i]['value'] != 'even'):
                                kefs.append(item['result']['odds'][i]['odds'])
                                kefs.append(item['result']['odds'][i]['value'])
                        if len(kefs) > 0:
                            bet_total = bet_list_copy.copy()
                            bet_total.append('1-я карта')
                            total_map = 'Тотал Б (' + str(kefs[1])[1:] +')'
                            bet_total.append(total_map)
                            if kefs[1].startswith('>'):
                                kefs_total = [kefs[0], kefs[2]]
                                bet_total.append(kefs_total)
                            else:
                                kefs_total = [kefs[2], kefs[0]]
                                bet_total.append(kefs_total)
                            bet_total.append(current_time)
                            if len(bet_total) > 0:
                                bet_list_final.append(bet_total)
                        if len(kefs) > 4:
                            bet_total = bet_list_copy.copy()
                            bet_total.append('2-я карта')
                            total_map = 'Тотал Б (' + str(kefs[1])[1:] +')'
                            bet_total.append(total_map)
                            if kefs[5].startswith('>'):
                                kefs_total = [kefs[4], kefs[6]]
                                bet_total.append(kefs_total)
                            else:
                                kefs_total = [kefs[6], kefs[4]]
                                bet_total.append(kefs_total)
                            bet_total.append(current_time)
                            if len(bet_total) > 0:
                                bet_list_final.append(bet_total)
    return(bet_list_final)

async def get_urls(page):
    querystring = {"page": page[0], "match_type": page[1]}
    proxi = choice(['http://45.145.160.130:8000', 'http://138.124.186.18:8000', 'http://193.9.17.244:8000'])
    url = "https://vnimpvgameinfo.esportsworldlink.com/v2/match"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=querystring, proxy=proxi) as resp:
                if resp.status == 200:
                    resjs = await resp.json()
                    matches_id = [res['id'] for res in resjs['result'] if res['game_id'] in [151, 140, 70, 37197927]]
                else:
                    matches_id = []  # Пропустить обработку, если возникла ошибка
        except Exception as e:
            print(f"Произошла ошибка при получении данных: {e}")
            matches_id = []  # Пропустить обработку, если возникла ошибка
    return matches_id

async def get_json_matches(match_id):
    proxi = choice(['http://45.145.160.130:8000', 'http://138.124.186.18:8000', 'http://193.9.17.244:8000'])
    querystring = {"match_id": match_id}
    url = "https://vnimpvgameinfo.esportsworldlink.com/v2/odds"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=querystring, proxy=proxi) as resp:
            match_json = await resp.json()
    return [match_json]

async def raybet():
    pages = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (1, 1), (2, 1), (1, 0), (2, 0), (3, 0), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
             (7, 3), (8, 3)]
    tasks = [get_urls(page) for page in pages]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    matches_id = list(itertools.chain.from_iterable(results))
    tasks = [get_json_matches(match_id) for match_id in matches_id]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    matches_jsons = list(itertools.chain.from_iterable(results))
    return get_coef(matches_jsons)




if __name__ == '__main__':
    print(*asyncio.run(raybet()), sep='\n')
