import requests
from datetime import datetime as dt
# Название бк, название игры, название турнира, Команда1, команда2, дата_начала, матч/карта1/карта2, победа/тб/фора/фб/ф10, кофы, дата_запроса

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

    responsel = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    tourid = [ci['id'] for ci in responsel.json()['sports'] if 'Итоги турнира' not in ci['name']]

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
    print('\nПодгрузка  матчей в линии произошла успешно...\n')
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
    print('\nПодгрузка матчей в лайве произошла успешно...\n')
    return response

# получение нужных данных с фонбет
def get_value(x):
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
            print(bd1)

get_value(fonbet_line())