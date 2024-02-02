import requests
import time
from datetime import datetime as dt
from datetime import timedelta as td

now = dt.now()
current_time = now.strftime("%d.%m.%Y %H:%M:%S")
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime((time.strptime(current_time, pattern))))
current_time = now.strftime("%H:%M")

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
y = get_line_cloud(epoch, current_time, False)
print(*y,sep='\n')
stop = time.time()
print(stop - start)