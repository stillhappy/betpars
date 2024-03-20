import requests
from datetime import datetime
from datetime import timedelta
import asyncio
import aiohttp
import itertools
import json
from filtertour import filterteam, filtertourn
from fake_useragent import UserAgent
from random import choice

def get_final_live(event_result_final):
    bet_list_final = []
    game_name = {'CS 2': 'Counter-Strike', 'League of Legends': 'LoL'}
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    date_format = '%Y-%m-%d %H:%M'
    initial_date = datetime.strptime(current_time, date_format)
    updated_date = initial_date + timedelta(hours=3)
    current_time = updated_date.strftime(date_format)

    for event in event_result_final:
        item = event['Value']
        for i in item:
            sg_value = i.get('SG')
            if sg_value is not None and len(sg_value) > 0:
                bet_list = []
                bet_list.append('live')
                bet_list.append('1x')
                game_check = i['L'].split('.')[0]
                if game_check in game_name:
                    game_check = game_name[game_check]
                bet_list.append(game_check)
                bet_list.append(i['L'].split('.')[1])
                team1 = i['O1'].rstrip().lower().title().replace('Club', '').replace(
                    'Team', '').replace(
                    'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                               ' ').replace(
                    'Challengers', '').replace('Chall', '').strip()
                team2 = i['O2'].rstrip().lower().title().replace('Club', '').replace(
                    'Team', '').replace(
                    'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                               ' ').replace(
                    'Challengers', '').replace('Chall', '').strip()
                bet_list.append(filterteam.get(team1, team1))
                bet_list.append(filterteam.get(team2, team2))
                bet_list.append(datetime.fromtimestamp(i['S']).strftime('%Y-%m-%d %H:%M'))
                bet_list_copy = bet_list.copy()
                bet_list.append('Общая')
                bet_list.append('Исходы')
                kef = []
                for node in i['E']:
                    if node['T'] == 1:
                        kef.append(node['C'])
                    if node['T'] == 2:
                        kef.append(node['C'])
                    if node['T'] == 3:
                        kef.append(node['C'])
                bet_list.append(kef)
                bet_list.append(current_time)
                if len(bet_list[9]) > 1:
                    bet_list_final.append(bet_list)
        for i in item:
                try:
                    bets = i['SG']
                except KeyError:
                    continue
                kef = []
                for node in bets:
                    for item in node['E']:
                        if item['T'] == 1:
                            kef.append(item['C'])
                        if item['T'] == 3:
                            kef.append(item['C'])

                if len(kef) > 0:
                    bet_map = bet_list_copy.copy()
                    kef_map = [kef[0],kef[1]]
                    bet_map.append('1-я карта')
                    bet_map.append('Исходы')
                    bet_map.append(kef_map)
                    bet_map.append(current_time)
                    if len(bet_map[9]) > 1:
                        bet_list_final.append(bet_map)
                if len(kef) > 2:
                    bet_map = bet_list_copy.copy()
                    kef_map = [kef[2],kef[3]]
                    bet_map.append('2-я карта')
                    bet_map.append('Исходы')
                    bet_map.append(kef_map)
                    bet_map.append(current_time)
                    if len(bet_map[9]) > 1:
                        bet_list_final.append(bet_map)
                if len(kef) > 4:
                    bet_map = bet_list_copy.copy()
                    kef_map = [kef[4],kef[5]]
                    bet_map.append('3-я карта')
                    bet_map.append('Исходы')
                    bet_map.append(kef_map)
                    bet_map.append(current_time)
                    if len(bet_map[9]) > 1:
                        bet_list_final.append(bet_map)
                kef = []
                for node in bets:
                    for item in node['E']:
                        if item['T'] == 7:
                            kef.append(item['C'])
                            kef.append(item['P'])
                        if item['T'] == 8:
                            kef.append(item['C'])

                if len(kef) > 0:
                    bet_fora = bet_list_copy.copy()
                    kef_fora = [kef[0],kef[2]]
                    bet_fora.append('1-я карта')
                    if '-' in str(kef[2]):
                        kef_fora = [kef[0], kef[1]]
                        bet_fora.append('Фора 1 (' + str(kef[2]) + ')')
                    else:
                        if 95 <= ((1/kef[0])*100 + (1/kef[2])*100 - 7.52) <= 105:
                            bet_fora.append('Фора 1 (' + str(kef[1]) + ')')
                        else:
                            kef_fora = [kef[0], kef[1]]
                            bet_fora.append('Фора 1 (' + str(kef[2]) + ')')
                    bet_fora.append(kef_fora)
                    bet_fora.append(current_time)
                    if len(bet_fora[9]) > 1:
                        bet_list_final.append(bet_fora)
                if len(kef) > 3:
                    bet_fora = bet_list_copy.copy()
                    kef_fora = [kef[3],kef[5]]
                    bet_fora.append('2-я карта')
                    if '-' in str(kef[5]):
                        kef_fora = [kef[3], kef[4]]
                        bet_fora.append('Фора 1 (' + str(kef[5]) + ')')
                    else:
                        if 95 <= ((1/kef[3])*100 + (1/kef[5])*100 - 7.52) <= 105:
                            bet_fora.append('Фора 1 (' + str(kef[4]) + ')')
                        else:
                            kef_fora = [kef[3], kef[4]]
                            bet_fora.append('Фора 1 (' + str(kef[5]) + ')')
                    bet_fora.append(kef_fora)
                    bet_fora.append(current_time)
                    if len(bet_fora[9]) > 1:
                        bet_list_final.append(bet_fora)
                if len(kef) > 6:
                    bet_fora = bet_list_copy.copy()
                    kef_fora = [kef[6],kef[8]]
                    bet_fora.append('3-я карта')
                    if '-' in str(kef[8]):
                        kef_fora = [kef[6], kef[7]]
                        bet_fora.append('Фора 1 (' + str(kef[8]) + ')')
                    else:
                        if 95 <= ((1/kef[6])*100 + (1/kef[8])*100 - 7.52) <= 105:
                            bet_fora.append('Фора 1 (' + str(kef[7]) + ')')
                        else:
                            kef_fora = [kef[6], kef[7]]
                            bet_fora.append('Фора 1 (' + str(kef[8]) + ')')
                    bet_fora.append(kef_fora)
                    bet_fora.append(current_time)
                    if len(bet_fora[9]) > 1:
                        bet_list_final.append(bet_fora)

                kef = []
                for node in bets:
                    for item in node['E']:
                        if item['T'] == 9:
                            kef.append(item['C'])
                            kef.append(item['P'])
                        if item['T'] == 10:
                            kef.append(item['C'])

                if len(kef) > 0:
                    bet_total = bet_list_copy.copy()
                    kef_total = [kef[0], kef[2]]
                    bet_total.append('1-я карта')
                    bet_total.append('Тотал Б (' + str(kef[1]) + ')')
                    bet_total.append(kef_total)
                    bet_total.append(current_time)
                    if len(bet_total[9]) > 1:
                        bet_list_final.append(bet_total)
                if len(kef) > 3:
                    bet_total = bet_list_copy.copy()
                    kef_total = [kef[3], kef[5]]
                    bet_total.append('2-я карта')
                    bet_total.append('Тотал Б (' + str(kef[4]) + ')')
                    bet_total.append(kef_total)
                    bet_total.append(current_time)
                    if len(bet_total[9]) > 1:
                        bet_list_final.append(bet_total)
                if len(kef) > 6:
                    bet_total = bet_list_copy.copy()
                    kef_total = [kef[6], kef[8]]
                    bet_total.append('3-я карта')
                    bet_total.append('Тотал Б (' + str(kef[7]) + ')')
                    bet_total.append(kef_total)
                    bet_total.append(current_time)
                    if len(bet_total[9]) > 1:
                        bet_list_final.append(bet_total)
    return bet_list_final

def get_urls(prox):

    params = {
        'sport': '40',
        'gr': '44',
        'country': '1',
        'partner': '51',
        'virtualSports': 'true',
    }
    proxi = choice(prox)
    proxies = {
        'http': proxi,
        'https': proxi
    }
    response = requests.get('https://funbets.shop/LiveFeed/GetChampsZip', params=params)

    champ_id = []
    for ci in response.json()['Value']:
        if 'League of Legends' == ci['SSN'] or 'Dota 2' == ci['SSN'] or 'CS 2' == ci['SSN'] or 'Valorant' == ci['SSN']:
            champ_id.append(ci['LI'])

    return champ_id

async def get_matches1x(champ_id, prox):
    params = {
        'sports': '40',
        'champs': champ_id,
        'count': '50',
        'gr': '44',
        'antisports': '188',
        'mode': '4',
        'subGames': '506672024',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true',
    }
    url = 'https://funbets.shop/LiveFeed/Get1x2_VZip'
    ua = UserAgent(min_percentage=1.5)
    proxi = choice(prox)

    async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:

                if resp.content_type != 'application/json' or resp.status != 200:
                    return []
                else:
                    resjs = await resp.json()
    return [resjs]

async def get_value(event, prox):
    url = event[0]
    querystring = event[1]
    proxi = choice(prox)
    async with aiohttp.ClientSession() as session:

            async with session.get(url, params=querystring) as resp:
                if resp.content_type != 'application/json' or resp.status != 200:
                    return []
                else:
                    resjs = await resp.json()

    return [resjs]

async def live1x():
    prox = ['http://45.145.160.130:8000', 'http://138.124.186.18:8000', 'http://193.9.17.244:8000']

    champ_ids = get_urls(prox)
    tasks = [get_matches1x(chid, prox) for chid in champ_ids]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    matches_id = list(itertools.chain.from_iterable(results))
    items = []
    for event in matches_id:
        for item in event['Value']:
            champs = (item['LI'])
            game_id = (item['I'])
            params = {
                'sports': '40',
                'champs': champs,
                'count': '50',
                'gr': '44',
                'antisports': '188',
                'mode': '4',
                'subGames': game_id,
                'country': '1',
                'partner': '51',
                'getEmpty': 'true',
            }
            items.append(('https://funbets.shop/LiveFeed/Get1x2_VZip', params))
    tasks = [get_value(item, prox) for item in items]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    event_result_final = list(itertools.chain.from_iterable(results))
    return get_final_live(event_result_final)

if __name__ == '__main__':
    print(*asyncio.run(live1x()), sep='\n')