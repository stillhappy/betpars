from datetime import datetime as dt
from datetime import timedelta as td
import time
import asyncio
import aiohttp
import itertools
from fake_useragent import UserAgent
from random import choice
import json
from filtertour import filterteam, filtertourn
import pytz

def get_odds(markets):
    now = dt.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    date_format = '%Y-%m-%d %H:%M'
    initial_date = dt.strptime(current_time, date_format)
    updated_date = initial_date + td(hours=3)
    current_time = updated_date.strftime(date_format)
    bdtf = []
    game_dct = {'Dota 2': 'Dota 2', 'CS:GO': 'Counter-Strike', 'League of Legends': 'LoL', 'Valorant': 'Valorant'}
    map_dct = {'MAP 1': '1-я карта', 'MAP 2': '2-я карта', 'MAP 3': '3-я карта', 'MAP 4': '4-я карта', 'MAP 5': '5-я карта'}
    bets_dct = {'WINNER': 'Исходы', 'WINNER (MAPS)': 'Исходы',
                'ROUND HANDICAP (INCL. OVERTIME)': 'Фора', 'TOTAL ROUNDS (INCL. OVERTIME)': 'Тотал', 'TOTAL KILLS OVER/UNDER': 'Тотал', 'TEAM TO DRAW FIRST BLOOD': 'Первая кровь',
                'RACE TO 10 KILLS': 'Гонка до 10 киллов'}
    global filtertourn
    for ci in markets:
        bdtf1 = []
        if ci['match_scoreline']:
            bdtf1.append('live')
        else:
            bdtf1.append('line')
        bdtf1.append('TF')
        if ci['game_name'] in game_dct:
            bdtf1.append(game_dct[ci['game_name']])
        else:
            continue
        bdtf1.append(filtertourn.get(ci['competition_name'].rstrip(' Spring').replace('2024 ', '').strip(), ci['competition_name'].rstrip(' Spring').replace('2024 ', '').strip()))
        if 'Challengers' in bdtf1[-1] and bdtf1[-2] == 'Valorant':
            bdtf1[-1] = 'Challengers League'
        if 'Champions' in bdtf1[-1] and bdtf1[-2] == 'Valorant':
            bdtf1[-1] = 'Champions Tour'
        global filterteam
        team1 = ci['home']['team_name'].rstrip().lower().title().replace('Club', '').replace('Team', '').replace('Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ', ' ').strip()
        team2 = ci['away']['team_name'].rstrip().lower().title().replace('Club', '').replace('Team', '').replace('Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ', ' ').strip()
        bdtf1.append(filterteam.get(team1, team1))
        bdtf1.append(filterteam.get(team2, team2))
        bdtf1.append(dt.strptime(ci['start_datetime'], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M'))
        if ci['markets'][0]['market_option'] == 'match':
            bdtf1.append('Общая')
        else:
            bdtf1.append(map_dct[ci['markets'][0]['map_option']])
        for sh, k in enumerate(ci['markets']):
            if ci['game_name'] == 'Dota 2':
                if sh > 22:
                    break
                if sh not in [0, 1, 2, 20, 21]:
                    continue
            else:
                if sh > 2:
                    break
            bdtf2 = bdtf1.copy()
            if k['market_type_name'] in bets_dct:
                if k['selection'][0]['status'] == 'open':
                    bdtf2.append(bets_dct[k['market_type_name']])
                    if bdtf2[-1] == 'Фора' or bdtf2[-1] == 'Тотал':
                        bdtf2[-1] = f"{bdtf2[-1]} ({k['selection'][0]['handicap']})"
                    bdtf2.append([s.get('euro_odds') for s in k['selection']])
                    bdtf2.append(current_time)
                    bdtf.append(bdtf2)
                else:
                    continue
    return bdtf

async def get_all_matches(timing, headers, querystring_common, url):
    proxi = choice(['http://138.124.186.18:8000', 'http://193.9.17.244:8000'])
    if timing[0] == 'inplay':
        querystring_common["timing"] = "inplay"
    elif timing[0] == 'early':
        querystring_common["timing"] = "early"
        querystring_common["date"] = timing[1]
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, params=querystring_common, proxy=proxi) as resp:
            if resp.status == 200 and resp.content_type == 'application/json':
                match_json = await resp.json()
            else:
                return []
    return match_json['results']

def get_id_markets_tf(results):
    id_markets = []
    for k in results:
        for ci in k:
            x = [ci['event_id']]
            for k in ci['market_tabs']:
                if k['open'] > 0:
                    x.append(k['tab_name'])
            if len(x) > 1:
                id_markets.append(x)
    return id_markets

async def get_urls(payload, url, headers):
    event_id = payload[0]
    markets = []
    proxi = choice(['http://138.124.186.18:8000', 'http://193.9.17.244:8000'])
    async with aiohttp.ClientSession() as session:
        for ci in payload[1:]:
            if ci != 'MATCH':
                map_option = ci
                market_option = ci.split()[0]
                querystring = {"event_id": event_id, "combo": "false", "outright": "false",
                               "sort_by_popular": "false",
                               "map_option": map_option, "market_option": market_option, "lang": "en",
                               "timezone": "Europe/Moscow"}
                async with session.post(url, headers=headers, params=querystring, proxy=proxi) as resp:
                    if resp.status == 200 and (await resp.json())['results'][0]:
                        markets.append((await resp.json())['results'][0])
                    else:
                        return []
            else:
                market_option = ci.split()[0]
                querystring = {"event_id": event_id, "combo": "false", "outright": "false",
                               "sort_by_popular": "false", "market_option": market_option, "lang": "en",
                               "timezone": "Europe/Moscow"}
                async with session.post(url, headers=headers, params=querystring, proxy=proxi) as resp:
                    if resp.status == 200 and (await resp.json())['results'][0]:
                        markets.append((await resp.json())['results'][0])
                    else:
                        return []
    return markets

async def tf():
    querystring_common = {
        "page_size": 100,
        "combo": "false",
        "outright": "false",
        "timing": "today",
        "sort_by_popular": "false",
        "market_option": "MATCH",
        "lang": "en",
        "timezone": "Europe/Moscow"
    }
    headers = {
        "authority": "api-v4.ely889.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Token 9278cadf62902610a21cfecfc60b8eeb2c830e93",
        "origin": "https://gc.ely889.com",
        "public-token": "b8c712a2f691483381abad76cef9f67d",
        "referer": "https://gc.ely889.com/",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tf-authorization": "fb58bd9c9802250b4bb8d00acd055dce6a0854422d699ef2b4c281a7baa0bdb818ab7119680b86ebb0f14493efa003ca121a86b9076f2f2ddfab9b9e1ea535d5",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)"
    }
    url = "https://api-v4.ely889.com/api/v4/events/paginate"
    vhod = [('inplay', 'now'), ('today', 'now'), ('early', (dt.now()).strftime("%Y-%m-%d")), ('early', (dt.now() + td(days=1)).strftime("%Y-%m-%d")), ('early', (dt.now() + td(days=2)).strftime("%Y-%m-%d")), ('early', (dt.now() + td(days=3)).strftime("%Y-%m-%d"))]
    tasks = [get_all_matches(timing, headers, querystring_common, url) for timing in vhod]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    payloads = get_id_markets_tf(results)
    tasks = [get_urls(payload, url, headers) for payload in payloads]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    combined_list = list(itertools.chain.from_iterable(results))
    return get_odds(combined_list)


if __name__ == '__main__':
    print(*asyncio.run(tf()), sep='\n')

