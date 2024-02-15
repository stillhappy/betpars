import requests
from datetime import datetime as dt
from datetime import timedelta as td
from filtertour import filterteam

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
    filfon = ['Наименьшее количество смертей в раунде', 'Итоги турнира', 'Наименьшее количество смертей в раунде',
              'Наибольший ADR', 'Карта с наибольшим % побед за T',
              'Карта с наибольшим % побед за CT', 'Наибольший % убийств в голову',
              'Команда с наибольшим количеством убийств на карте', 'Команда с наибольшим количеством сыгранных карт',
              'Карта с наибольшим % побед за T (атакующая сторона)',
              'Карта с наибольшим % побед за CT (сторона обороны)', 'Сравнения по киллам']
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
    filfon = ['Наименьшее количество смертей в раунде', 'Итоги турнира', 'Наименьшее количество смертей в раунде',
              'Наибольший ADR', 'Карта с наибольшим % побед за T',
              'Карта с наибольшим % побед за CT', 'Наибольший % убийств в голову',
              'Команда с наибольшим количеством убийств на карте', 'Команда с наибольшим количеством сыгранных карт',
              'Карта с наибольшим % побед за T (атакующая сторона)',
              'Карта с наибольшим % побед за CT (сторона обороны)', 'Сравнения по киллам']
    bd = []
    now = dt.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    for ci in x.json()['events']:
        bd0 = [ci['place'], 'Fonbet']
        if ci['sportName'].split('.')[-1].strip() in filfon:
            continue
        z = ci['sportName'].split('.')[:-1]
        if z[0] == 'Киберспорт':
            bd0.append(z[1].strip())
            bd0.append(z[2].strip())
        else:
            if len(z) < 2:
                continue
            bd0.append(z[0].strip())
            bd0.append(z[1].strip())
        global filterteam
        if not ci.get('team1') or not ci.get('team2'):
            continue
        team1 = ci['team1'].rstrip().lower().title().replace('Club', '').replace('Team', '').replace('Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ', ' ').strip()
        team2 = ci['team2'].rstrip().lower().title().replace('Club', '').replace('Team', '').replace('Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ', ' ').strip()
        bd0.append(filterteam.get(team1, team1))
        bd0.append(filterteam.get(team2, team2))
        cur_year = dt.now().year
        bd0.append(dt.strptime(f"{cur_year}.{ci['startTime']}", '%Y.%d.%m %H:%M').strftime('%Y-%m-%d %H:%M'))
        if ci['name'] != f'{ci["team1"]} – {ci["team2"]}':
            bd0.append(ci['name'])
        else:
            bd0.append('Общая')
        for j in ci['subcategories']:
            bd1 = bd0.copy()
            if j['name'] != 'Исходы':
                bd1.append(f'{j["name"]} {j["quotes"][0]['name']}')
                bd1.append([(k['value']) for k in j['quotes']])
            else:
                bd1.append(j['name'])
                bd1.append([(k['value']) for k in j['quotes']])
            bd1.append(current_time)
            bd.append(bd1)
    return bd

def fonbet():
    x = get_value_fonbet(fonbet_line()) + get_value_fonbet(fonbet_live())
    return x

if __name__ == "__main__":
    fonbet()