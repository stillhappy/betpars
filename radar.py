import requests
from bs4 import BeautifulSoup as bs
import lxml
from datetime import datetime as dt
from datetime import timedelta as td
import time

filfon = ['Наименьшее количество смертей в раунде', 'Итоги турнира', 'Наименьшее количество смертей в раунде', 'Наибольший ADR', 'Карта с наибольшим % побед за T',
          'Карта с наибольшим % побед за CT', 'Наибольший % убийств в голову', 'Команда с наибольшим количеством убийств на карте', 'Команда с наибольшим количеством сыгранных карт', 'Карта с наибольшим % побед за T (атакующая сторона)',
          'Карта с наибольшим % побед за CT (сторона обороны)']

now = dt.now()
current_time = now.strftime("%d.%m.%Y %H:%M:%S")
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime((time.strptime(current_time, pattern))))
current_time = now.strftime("%H:%M")

# парсер линии фонбета
def fonbet_line():
    url = "https://line07w.bk6bba-resources.com/line/mobile/showSports"

    querystring = {"sysId": "2", "lang": "ru", "lineType": "full_line", "skId": "29086", "scopeMarket": "1600"}

    payload = ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.fon.bet",
        "Referer": "https://www.fon.bet/mobile/bets/esports/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^"
    }
    global filfon
    responsel = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    tourid = []
    for ci in responsel.json()['sports']:
        if ci['name'].split('.')[-1].strip() not in filfon:
            tourid.append(ci['id'])
    url = "https://line07w.bk6bba-resources.com/line/mobile/showEvents"

    querystring = {"sysId": "2", "lang": "ru", "scopeMarket": "1600", "lineType": "full_line",
                   "sportId": []}
    querystring['sportId'] = tourid

    payload = ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.fon.bet",
        "Referer": "https://www.fon.bet/mobile/bets/esports/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response


# парсер лайва фонбета
def fonbet_live():
    url = "https://line08w.bk6bba-resources.com/line/mobile/showEvents"

    querystring = {"sysId": "2", "lang": "ru", "scopeMarket": "1600", "lineType": "live_line", "skId": "29086"}
    payload = ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.fon.bet",
        "Referer": "https://www.fon.bet/mobile/live/esports/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response

# получение нужных данных с фонбет
def get_value_fonbet(x):
    bd = []
    now = dt.now()
    current_time = now.strftime("%H:%M")
    for ci in x.json()['events']:
        bd0 = [ci['place'], 'Fonbet']
        z = ci['sportName'].split('.')[:-1]
        if z[0] == 'Киберспорт':
            bd0.append(z[1].strip())
            bd0.append(z[2].strip())
        else:
            if len(z) < 2:
                continue
            bd0.append(z[0].strip())
            bd0.append(z[1].strip())
        bd0.append(ci['team1'])
        bd0.append(ci['team2'])
        bd0.append(ci['startTime'])
        if ci['name'] != f'{ci["team1"]} – {ci["team2"]}':
            bd0.append(ci['name'])
        else:
            bd0.append('Общая')
        for j in ci['subcategories']:
            bd1 = bd0.copy()
            if j['name'] != 'Исходы':
                bd1.append(f'{j["name"]} {j["quotes"][0]['name']}')
                bd1.append(f'{j["quotes"][0]["value"]}; {j["quotes"][1]["value"]}')
            else:
                bd1.append(j['name'])
                bd1.append('; '.join([str(k['value']) for k in j['quotes']]))
            bd1.append(current_time)
            bd.append(bd1)
    return bd

# парсер линии 1х
def xbet_line():
    pass

# парсер лайва 1х
def xbet_live():
    pass

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

# Запрос ко всем кофам позитива по айди матча
def get_match_pos(event_id, session):
    url = "https://csgopositive.me/lib/bets.php"
    payload1 = f"action=get_koef&event_id={event_id}&team_id=1&lang=RU"
    payload2 = f"action=get_koef&event_id={event_id}&team_id=2&lang=RU"

    headers = {
        "cookie": "lang=RU; _ym_uid=1705850604685101510; _ym_d=1705850604; PHPSESSID=1e4d488657b9358298b19e2195aa3f35; fixed_chat=true; minimized_chat=true; _ym_isad=2; cf_clearance=vtr5UkokmAiDT3xoy7olXNNnlCXQ4lGkyPHCVqDx3rg-1706622830-1-ARRx40SmK9utFW4XVOVnOhtoUs/E2mSZg3Ag0BaS/pGI1St2u2XSp+RjzqAP5FNwkYDKTbmHJlHWDGJv43E7l5c=; auth=4d6a41354f475a6b4d6a41324d7a56694e545668596d51304d6a5a6c4d47497a4d7a41334e446c6b4f44633d; auth=4d6a41354f475a6b4d6a41324d7a56694e545668596d51304d6a5a6c4d47497a4d7a41334e446c6b4f44633d",
        "authority": "csgopositive.me",
        "accept": "*/*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://csgopositive.me",
        "referer": "https://csgopositive.me/",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)",
        "x-requested-with": "XMLHttpRequest"
    }
    response1 = session.post(url, data=payload1, headers=headers)
    response2 = session.post(url, data=payload2, headers=headers)
    soup1 = bs(response1.text, 'lxml')
    soup2 = bs(response2.text, 'lxml')
    return soup1, soup2

# парсер линии или лайва позитива
def get_line_live_pos(line_live):
    response = requests.get('https://csgopositive.me/')
    response.encoding = 'utf-8'
    bdpos = []
    now = dt.now()
    current_time = now.strftime("%H:%M")
    filterposbk = {'valorant': 'Valorant', 'lol': 'LoL', 'csgo': 'Counter-Strike', 'dota2': 'Dota 2'}
    dct = {'Победа в матче': 'Общая', 'Победа в серии BO3': 'Общая', 'Победа на карте #1': '1-я карта',
           'Победа на карте #2': '2-я карта', 'Победа на карте #3': '3-я карта', 'Победа на карте #4': '4-я карта',
           'Победа на карте #5': '5-я карта'}
    dct2 = {'Исходы': ['Победа в серии BO3', 'Победа на карте #1', 'Победа на карте #2', 'Победа на карте #3',
                       'Победа на карте #4', 'Победа на карте #5', 'Победа в матче'],
            'Сделают первое убийство': 'Первая кровь',
            'Сделают первыми 5 убийств': 'Гонка до 5 киллов', 'Сделают первыми 10 убийств': 'Гонка до 10 киллов',
            'больше 21.5': 'Тотал Б (21.5)', 'меньше 21.5': 'Тотал Б (21.5)', 'больше 20.5': 'Тотал Б (20.5)',
            'меньше 20.5': 'Тотал Б (20.5)'}
    if response.status_code == 200:
        soup = bs(response.text, 'lxml')
        if line_live == 'line':
            lst = soup.find(id='upcoming').find_all(class_='event')
            bdpos1 = ['line', 'csgopositive']
        else:
            lst = soup.find(id='current').find_all(class_='event')
            bdpos1 = ['live', 'csgopositive']
        for ci in lst:
            bdpos2 = bdpos1.copy()
            game = ci.get('class')
            gamex = 'x'
            if game[-1] == 'live_betting':
                gamex = game[-2].split('_')[0]
            else:
                gamex = game[-1].split('_')[0]
            if gamex not in filterposbk:
                continue
            bdpos2.append(filterposbk[gamex])
            bdpos2.append(ci.find('span', class_='event_name').text)
            if ci.find('span', class_='event_name').text in ['CS2 Positive duo aim ','CS2 Positive aim ']:
                continue
            bdpos2.append(ci.find_all('span', class_='team_name')[0].text)
            bdpos2.append(ci.find_all('span', class_='team_name')[1].text)
            data_match = dt.strptime(ci.find(class_='timer').get('data-start'), '%m/%d/%Y %H:%M:%S').strftime('%d.%m %H:%M')
            bdpos2.append(data_match)
            event_id = ci.get('data-id')
            session = requests.Session()
            a, b = get_match_pos(event_id, session)
            a1 = a.find_all(class_='koef')
            b1 = b.find_all(class_='koef')
            if not a1:
                continue
            x = a1[0].previous_sibling.text.strip()
            if x not in dct:
                continue
            for ci, cj in zip(a1, b1):
                bdpos3 = bdpos2.copy()
                if ci.previous_sibling.text.strip() != x and ci.previous_sibling.text.strip() in dct:
                    x = ci.previous_sibling.text.strip()

                if ci.previous_sibling.text.strip() == x:
                    bdpos3.append(dct[ci.previous_sibling.text.strip()])
                    bdpos3.append('Исходы')
                    bdpos3.append([ci.text, cj.text])
                    bdpos3.append(current_time)
                if ci.previous_sibling.text.strip() != x and ci.previous_sibling.text.strip() not in dct and ci.previous_sibling.text.strip() in dct2:
                    if ci.previous_sibling.text.strip() in ['больше 21.5', 'больше 20.5']:
                        bdpos3.append(dct[x])
                        bdpos3.append(dct2[ci.previous_sibling.text.strip()])
                        bdpos3.append([ci.text])

                    elif ci.previous_sibling.text.strip() in ['меньше 21.5', 'меньше 20.5']:
                        bdpos[-1][-1].append(cj.text)
                        bdpos3.append(current_time)
                        continue
                    else:
                        bdpos3.append(dct[x])
                        bdpos3.append(dct2[ci.previous_sibling.text.strip()])
                        bdpos3.append([ci.text, cj.text])
                        bdpos3.append(current_time)

                if len(bdpos3) > 7:
                    bdpos.append(bdpos3)
    return bdpos

# парсер линии рейбета
def raybet_line():
    pass

# парсер лайва рейбета
def raybet_live():
    pass

# запрос к игре клаудбет
def get_game_cloud(game, epoch, live=False):
    if live:
        url = f'https://sports-api.cloudbet.com/pub/v2/odds/events?sport={game}&live=true&limit=10000'
    else:
        url = f"https://sports-api.cloudbet.com/pub/v2/odds/events?sport={game}&from={epoch}&to={epoch+345600}&live=false&limit=10000"
    headers = {
        "accept": "application/json",
        "X-API-Key": "eyJhbGciOiJSUzI1NiIsImtpZCI6IkhKcDkyNnF3ZXBjNnF3LU9rMk4zV05pXzBrRFd6cEdwTzAxNlRJUjdRWDAiLCJ0eXAiOiJKV1QifQ.eyJhY2Nlc3NfdGllciI6InRyYWRpbmciLCJleHAiOjIwMjIxOTM0OTQsImlhdCI6MTcwNjgzMzQ5NCwianRpIjoiOWFjMDA5ZTgtOTUwOC00ODQ1LWIxNWUtYjI0NTYwOWIzZTE4Iiwic3ViIjoiYzgzNmExMzAtNzUwYy00Mzk4LTk5YjgtNGZjYjMwZjcyZmYzIiwidGVuYW50IjoiY2xvdWRiZXQiLCJ1dWlkIjoiYzgzNmExMzAtNzUwYy00Mzk4LTk5YjgtNGZjYjMwZjcyZmYzIn0.D0sqjKbyR73CEJ2P_h-Dic46QOQtZUScYz32UOGk1T5GfQlEyXvUO_zjW2o4M4wkTgPNel8Y_rL0Nk1IvLnY_WICNUXm_1owp1vDjIc4erVfEW7IwyzKWqFw_AHjPaYj8JlZmKEhUPFazS2C_KzHwR3NeIRbQ06L1cnQQUXxjw4Fn9XPwmxdVA-0CAz--eNQ9Q_P4kKaTkn4e_Kub9WAhaoCfQVkGKTLRtSdbnS3gf9tP91edX74sKrwHysH_YRn6qFYl5oO98fXc9RR7lVq4XaOuRN3gcYjCz-dgR1peGL48xfsgr7RX3FVSWnElU9PtdzJfpgWYaLEDO2MqfhsHg"
    }
    return requests.request('GET', url, headers=headers).json()

# сбор даннных с клаудбет
def get_line_cloud(epoch, current_time, live):
    games = {'counter-strike': 'Counter-Strike', 'dota-2': 'Dota 2', 'league-of-legends': 'LoL', 'esport-valorant': 'Valorant'}
    bdcs = []
    dct = {'map1': '1-я карта', 'map2': '2-я карта', 'map3': '3-я карта', 'map4': '4-я карта', 'map5': '5-я карта'}
    for ci in games:
        response_game = get_game_cloud(ci, epoch, live)
        for k in response_game['competitions']:
            if k['name'] == 'The International':
                continue
            bdcs1 = ['line', 'Cloudbet', games[ci], k['name']]
            for i in k['events']:
                bdcs2 = bdcs1.copy()
                bdcs2.append(i['home']['name'])
                bdcs2.append(i['away']['name'])
                bdcs2.append((dt.strptime(i['cutoffTime'], "%Y-%m-%dT%H:%M:%SZ") + td(hours=3)).strftime("%d.%m %H:%M"))
                for j in i['markets']:
                    x = i['markets'][j]
                    if j.split('.')[1] == 'correct_score_in_maps':
                        continue
                    elif j.split('.')[1] in ['match_odds', 'winner']:
                        bdcs3 = bdcs2.copy()
                        bdcs3.append('Общая')
                        bdcs3.append('Исходы')
                        bdcs3.append([elem['price'] for elem in x['submarkets']['period=default']['selections']])
                        bdcs3.append(current_time)
                        bdcs.append(bdcs3)
                        continue
                    elif j.split('.')[1] in ['map_winner', 'map_winner_v2']:
                        for item in x['submarkets']:
                            bdcs3 = bdcs2.copy()
                            bdcs3.append(dct[item[-4:]])
                            bdcs3.append('Исходы')
                            bdcs3.append([a['price'] for a in x['submarkets'][item]['selections']])
                            bdcs3.append(current_time)
                            bdcs.append(bdcs3)
                        continue
                    elif j.split('.')[1] == 'map_round_handicap':
                        for itm in x['submarkets']:
                            for li, l in enumerate(x['submarkets'][itm]['selections']):
                                if li % 2 == 0:
                                    bdcs3 = bdcs2.copy()
                                    bdcs3.append(dct[itm[-4:]])
                                    if x['submarkets'][itm]['selections'][li]['params'][9:13][-1] == '&':
                                        bdcs3.append(f'Фора 1 (+{x['submarkets'][itm]['selections'][li]['params'][9:12]})')
                                    else:
                                        bdcs3.append(f'Фора 1 ({x['submarkets'][itm]['selections'][li]['params'][9:13]})')
                                    bdcs3.append([x['submarkets'][itm]['selections'][li]['price']])
                                else:
                                    bdcs3[-1].append(x['submarkets'][itm]['selections'][li]['price'])
                                    bdcs.append(bdcs3)
                    elif j.split('.')[1] == 'map_total_rounds':
                        for itm in x['submarkets']:
                            for li, l in enumerate(x['submarkets'][itm]['selections']):
                                if li % 2 == 0:
                                    bdcs3 = bdcs2.copy()
                                    bdcs3.append(dct[itm[-4:]])
                                    bdcs3.append(f'Тотал ({x['submarkets'][itm]['selections'][li]['params'][-4:]})')
                                    bdcs3.append([x['submarkets'][itm]['selections'][li]['price']])
                                else:
                                    bdcs3[-1].append(x['submarkets'][itm]['selections'][li]['price'])
                                    bdcs.append(bdcs3)

    return bdcs





start = time.time()
fon_line = get_value_fonbet(fonbet_line())
# fon_live = get_value_fonbet(fonbet_live())
# tf_line = get_value_tf(get_live_line_tf('line'))
# tf_live = get_value_tf(get_live_line_tf('live'))
# tf_next = get_value_tf(get_live_line_tf('next'))
# tf_next_next = get_value_tf(get_live_line_tf('next_next'))
# pos_line = get_line_live_pos('line')
# pos_live = get_line_live_pos('live')
# cloud_line = get_line_cloud(epoch, current_time, False)
# cloud_live = get_line_cloud(epoch, current_time, True)
stop = time.time()
# print(*fon_live,sep='\n')
# print(*tf_live, sep='\n')
# print(*pos_live, sep='\n')
# print(*cloud_live, sep='\n')
print(*fon_line,sep='\n')
# print(*tf_line, sep='\n')
# print(*tf_next, sep='\n')
# print(*tf_next_next, sep='\n')
# print(*pos_line, sep='\n')
# print(*cloud_line, sep='\n')
print(stop - start)