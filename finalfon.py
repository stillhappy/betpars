import requests

# функция для получения айди всех турниров в киберспорте в линии
def get_id_tur():
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

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    test = []
    for ci in response.json()['sports']:
        if 'Итоги турнира' in ci['name']:
            continue
        if input(f'{ci["name"]}. Добавить? да/нет') == 'да':
            test.append(ci['id'])
        else:
            continue
    return test

# функция запроса по турнирам в линии
def get_json(lst):
    url = "https://line07w.bk6bba-resources.com/line/mobile/showEvents"

    querystring = {"sysId": "2", "lang": "ru", "scopeMarket": "1600", "lineType": "full_line",
                   "sportId": []}
    querystring['sportId'] = lst

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

# функция запроса по турнирам в лайве
def get_json_live():
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

# получение значений коэффициентов
def get_value(x):
    for ci in x.json()['events']:
        print(f'\nТурнир: {ci["sportName"]}\n{ci["team1"]} - {ci["team2"]}\n{ci['name']}\nКолличество возможных маркетов: {len(ci["subcategories"])}')
        for cj in ci['subcategories']:
            print(f'\n{cj["name"]}: ',end=' ')
            x = cj['quotes']
            print(f'{x[0]['name']} ({x[0]['value']} - {x[1]["value"]}) {x[1]["name"]}',end='')

get_value(get_json_live())

# Название бк, название игры, название турнира, Команда1, команда2, дата_начала, матч/карта1/карта2, победа/тб/фора/фб/ф10, кофы, дата_запроса
