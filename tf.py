import requests
from datetime import datetime as dt
from datetime import timedelta as td
import time

# парсер линии или лайва тф
def get_live_line_tf(live_or_line_or_next):
    url = "https://api-v4.ely889.com/api/v4/events/paginate"

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

    querystring_common = {
        "combo": "false",
        "outright": "false",
        "timing": "today",
        "sort_by_popular": "true",
        "market_option": "MATCH",
        "lang": "en",
        "timezone": "Europe/Moscow"
    }

    if live_or_line_or_next == 'live':
        querystring_common["timing"] = "inplay"
    elif live_or_line_or_next == 'next':
        next_day = dt.now() + td(days=1)
        querystring_common["timing"] = "early"
        querystring_common["date"] = next_day.strftime("%Y-%m-%d")
    elif live_or_line_or_next == 'next_next':
        next_next_day = dt.now() + td(days=2)
        querystring_common["timing"] = "early"
        querystring_common["date"] = next_next_day.strftime("%Y-%m-%d")

    response = requests.get(url, headers=headers, params=querystring_common)
    return response.json()

# получение нужных данных с тф
def get_value_tf(x):
    bdtf = []
    now = dt.now()
    current_time = now.strftime("%H:%M")
    dct = {'MATCH': 'Общая', 'MAP 1': '1-я карта', 'MAP 2': '2-я карта', 'MAP 3': '3-я карта', 'MAP 4': '4-я карта', 'MAP 5': '5-я карта', 'WINNER': 'Исходы', 'WINNER (MAPS)': 'Исходы',
           'ROUND HANDICAP (INCL. OVERTIME)': 'Фора', 'TOTAL ROUNDS (INCL. OVERTIME)': 'Тотал', 'TOTAL KILLS OVER/UNDER': 'Тотал', 'TEAM TO DRAW FIRST BLOOD': 'Первая кровь',
           'RACE TO 10 KILLS': 'Гонка до 10 киллов'}
    for ci in x['results']:
        if ci['game_name'] not in ['CS:GO', 'League of Legends', 'Dota 2', 'Valorant', 'Call of Duty']:
            continue
        if ci['match_scoreline']:
            bdtf0 = ['live', 'tf']
        else:
            bdtf0 = ['line', 'tf']
        bdtf0.append(ci['game_name'])
        bdtf0.append(ci['competition_name'].replace('2024 ',''))
        bdtf0.append(ci['home']['team_name'])
        bdtf0.append(ci['away']['team_name'])
        date_str = ci['start_datetime']
        date_obj = dt.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        new_date_obj = date_obj - td(hours=5)
        formatted_date = new_date_obj.strftime('%d.%m %H:%M')
        bdtf0.append(formatted_date)
        tf_match = ci['market_tabs']
        with requests.Session() as rs:
            for j in tf_match:
                if j['open'] < 1:
                    continue
                evet_id = ci['event_id']
                market_option = j['tab_name']
                url = "https://api-v4.ely889.com/api/v4/events/paginate"
                map_option = market_option
                if market_option.split()[0] != map_option:
                    querystring = {"event_id": evet_id, "combo": "false", "outright": "false",
                                   "sort_by_popular": "false",
                                   "map_option": map_option, "market_option": market_option.split()[0], "lang": "en",
                                   "timezone": "Europe%2FMoscow"}
                else:
                    querystring = {"event_id": evet_id, "combo": "false", "outright": "false",
                                   "sort_by_popular": "false", "market_option": market_option.split()[0], "lang": "en",
                                   "timezone": "Europe%2FMoscow"}

                headers = {
                    "authority": "api-v4.ely889.com",
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "authorization": "Token 9278cadf62902610a21cfecfc60b8eeb2c830e93",
                    "ehcacun": "97cd6921a1fcc08e2809",
                    "origin": "https://gc.ely889.com",
                    "public-token": "b8c712a2f691483381abad76cef9f67d",
                    "referer": "https://gc.ely889.com/",
                    "sec-ch-ua": "^\\^Not_A",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "^\\^Windows^^",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "tf-authorization": "9f368339bd782879953fecfd341c92ad3fd01b95c2d2b9749e8befc709eb11b421460a0e6f568c76945ade88a7efd2b288fc494aa793b6dd32cc81bf3ee18fe3",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)"
                }
                response = rs.get(url, headers=headers, params=querystring)
                if response.status_code == 200 and response.json()['results'][0]:
                    info = response.json()['results'][0]
                    bdtf1 = bdtf0.copy()
                    bdtf1.append(dct[j['tab_name']])
                    bdtf2 = bdtf1.copy()
                    for sh, k in enumerate(info['markets']):
                        if info['game_name'] == 'Dota 2':
                            if sh > 22:
                                break
                            if sh not in [0,1,2,20,21]:
                                continue
                        else:
                            if sh > 2:
                                break
                        bdtf2 = bdtf1.copy()
                        if k['market_type_name'] in dct:
                            if k['selection'][0]['status'] == 'open':
                                bdtf2.append(dct[k['market_type_name']])
                                if bdtf2[-1] == 'Фора' or bdtf2[-1] == 'Тотал':
                                    bdtf2[-1] = f"{bdtf2[-1]} ({k['selection'][0]['handicap']})"
                                bdtf2.append([s.get('euro_odds') for s in k['selection']])
                                bdtf2.append(current_time)
                                bdtf.append(bdtf2)
                            else:
                                continue
    return bdtf

start = time.time()
print(*get_value_tf(get_live_line_tf('live')), sep='\n')
stop = time.time()
print(stop - start)