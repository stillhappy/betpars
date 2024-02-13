import requests
from datetime import datetime as dt
from datetime import timedelta as td
import time
import asyncio
import aiohttp
import itertools
from fake_useragent import UserAgent
from random import choice
import json

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

def get_live_line_tf(live_or_line_or_next):
    global headers
    global url
    results = []
    payload = ""
    querystring_common = {
        "combo": "false",
        "outright": "false",
        "timing": "today",
        "sort_by_popular": "false",
        "market_option": "MATCH",
        "lang": "en",
        "timezone": "Europe/Moscow"
    }

    if live_or_line_or_next == 'live':
        querystring_common["timing"] = "inplay"
        results = results + requests.request("GET", url, data=payload, headers=headers, params=querystring_common).json()['results']
    else:
        results = results + requests.request("GET", url, data=payload, headers=headers, params=querystring_common).json()['results']
        next_day = dt.now() + td(days=1)
        querystring_common["timing"] = "early"
        querystring_common["date"] = next_day.strftime("%Y-%m-%d")
        results = results + requests.request("GET", url, data=payload, headers=headers, params=querystring_common).json()['results']
        next_next_day = dt.now() + td(days=2)
        querystring_common["date"] = next_next_day.strftime("%Y-%m-%d")
        results = results + requests.request("GET", url, data=payload, headers=headers, params=querystring_common).json()['results']
        next_next_day = dt.now() + td(days=3)
        querystring_common["date"] = next_next_day.strftime("%Y-%m-%d")
        results = results + requests.request("GET", url, data=payload, headers=headers, params=querystring_common).json()['results']

    return results


def get_id_markets_tf(results):
    id_markets = []
    for ci in results:
        x = [ci['event_id']]
        for k in ci['market_tabs']:
            if k['open'] > 0:
                x.append(k['tab_name'])
        if len(x) > 1:
            id_markets.append(x)
    return id_markets

def get_odds(markets):
    now = dt.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    bdtf = []
    game_dct = {'Dota 2': 'Dota 2', 'CS:GO': 'Counter-Strike', 'League of Legends': 'LoL', 'Valorant': 'Valorant'}
    map_dct = {'MAP 1': '1-я карта', 'MAP 2': '2-я карта', 'MAP 3': '3-я карта', 'MAP 4': '4-я карта', 'MAP 5': '5-я карта'}
    bets_dct = {'WINNER': 'Исходы', 'WINNER (MAPS)': 'Исходы',
                'ROUND HANDICAP (INCL. OVERTIME)': 'Фора', 'TOTAL ROUNDS (INCL. OVERTIME)': 'Тотал', 'TOTAL KILLS OVER/UNDER': 'Тотал', 'TEAM TO DRAW FIRST BLOOD': 'Первая кровь',
                'RACE TO 10 KILLS': 'Гонка до 10 киллов'}
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
        bdtf1.append(ci['competition_name'])
        bdtf1.append(ci['home']['team_name'])
        bdtf1.append(ci['away']['team_name'])
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


async def get_url(payload):
    global url, headers
    event_id = payload[0]
    markets = []
    async with aiohttp.ClientSession() as session:
        for ci in payload[1:]:
            if ci != 'MATCH':
                map_option = ci
                market_option = ci.split()[0]
                querystring = {"event_id": event_id, "combo": "false", "outright": "false",
                               "sort_by_popular": "false",
                               "map_option": map_option, "market_option": market_option, "lang": "en",
                               "timezone": "Europe/Moscow"}
                async with session.post(url, headers=headers, params=querystring) as resp:
                    if resp.status == 200 and (await resp.json())['results'][0]:
                        markets.append((await resp.json())['results'][0])
            else:
                market_option = ci.split()[0]
                querystring = {"event_id": event_id, "combo": "false", "outright": "false",
                               "sort_by_popular": "false", "market_option": market_option, "lang": "en",
                               "timezone": "Europe/Moscow"}
                async with session.post(url, headers=headers, params=querystring) as resp:
                    if resp.status == 200 and (await resp.json())['results'][0]:
                        markets.append((await resp.json())['results'][0])
    return markets

async def tf():
    start = time.time()
    tasks = [get_url(payload) for payload in get_id_markets_tf(get_live_line_tf('line')) + get_id_markets_tf(get_live_line_tf('live'))]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    combined_list = list(itertools.chain.from_iterable(results))
    print(*get_odds(combined_list), sep='\n')
    stop = time.time()
    print(stop - start)

if __name__ == '__main__':
    asyncio.run(tf())