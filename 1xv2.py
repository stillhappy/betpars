import requests
from _datetime import datetime


bet_list = []
def get_final_line(event_result_final, game_id):

    bet_list =[]
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    for event in event_result_final['Value']:
        bet_event = []
        current_id = event['I']
        if current_id == game_id:

            bets = event['E']
            bet_event.append('line')
            bet_event.append('1x')
            game_name = event['L'].split('.')[0]
            if game_name == 'CS 2':
                game_name = 'Counter-Strike'
            if game_name == 'League of Legends':
                game_name = 'LoL'
            bet_event.append(game_name)
            bet_event.append(event['L'].split('.')[1])
            bet_event.append(event['O1'])
            bet_event.append(event['O2'])
            bet_event.append(datetime.fromtimestamp(event['S']).strftime('%d.%m %H:%M'))
            bet_event.append('Общая')
            bet_event.append('Исходы')
            coefs = []
            for item in bets:
                if 1 == item['T']:
                    coef1 = item['C']
                    coefs.append(coef1)
                if 2 == item['T']:
                    coef2 = item['C']
                    coefs.append(coef2)
                if 3 == item['T']:
                    coef3 = item['C']
                    coefs.append(coef3)
            bet_event.append(coefs)
            bet_event.append(current_time)
            if len(coefs) > 0:
                bet_list.append(bet_event)

        # Получение списков с форами
        if current_id == game_id:
            bet_fora_d = {}
            bet_fora_d['Название матча'] = event['L']
            bet_fora_d['Team 1'] = event['O1']
            bet_fora_d['Team 2'] = event['O2']
            bet_fora_d['Время'] = event['S']
            try:
                bets = event['SG']
            except KeyError:
                continue
            for item in bets:
                bet = item['PN']
                map = ''
                coefs = []
                for node in item['E']:
                    table_cell = node['T']
                    map = item['PN']
                    bet_fora_d['Карта'] = map
                    if 7 == table_cell:
                        fora = node['P']
                        fora = str(fora)
                        if fora.startswith('-'):
                            bet_fora_d['Исход'] = 'Фора 1 (' + str(fora) + ')'
                        else:
                            fora ='+' + fora
                            bet_fora_d['Исход'] = 'Фора 1 (' + str(fora) + ')'
                        coef1 = node['C']

                        coefs.append(coef1)
                    if 8 == table_cell:
                        fora = node['P']
                        coef2 = node['C']
                        coefs.append(coef2)
                bet_fora = []
                bet_fora.append('line')
                bet_fora.append('1x')
                game_name = event['L'].split('.')[0]
                if game_name == 'CS 2':
                    game_name = 'Counter-Strike'
                if game_name == 'League of Legends':
                    game_name = 'LoL'
                bet_fora.append(game_name)
                bet_fora.append(event['L'].split('.')[1])
                bet_fora.append(event['O1'])
                bet_fora.append(event['O2'])
                bet_fora.append(datetime.fromtimestamp(event['S']).strftime('%d.%m %H:%M'))
                bet_fora.append(map)
                if 'Исход' in bet_fora_d:
                    bet_fora.append(bet_fora_d['Исход'])

                bet_fora.append(coefs)
                bet_fora.append(current_time)

                if len(coefs) > 0:
                    bet_list.append(bet_fora)
        # Получение списков с тоталами
        if current_id == game_id:
            bet_total_d = {}
            bet_total_d['Название матча'] = event['L']
            bet_total_d['Team 1'] = event['O1']
            bet_total_d['Team 2'] = event['O2']
            bet_total_d['Время'] = event['S']
            try:
                bets = event['SG']
            except KeyError:
                continue
            for item in bets:
                bet = item['PN']
                map = ''
                coefs = []
                for node in item['E']:
                    table_cell = node['T']
                    map = item['PN']
                    bet_total_d['Карта'] = map
                    if 9 == table_cell:
                        total = node['P']
                        coef1 = node['C']
                        bet_total_d['Исход'] = 'Тотал Б (' + str(total) +')'
                        coefs.append(coef1)
                    if 10 == table_cell:
                        coef2 = node['C']
                        coefs.append(coef2)
                bet_total = []
                bet_total.append('line')
                bet_total.append('1x')
                game_name = event['L'].split('.')[0]
                if game_name == 'CS 2':
                    game_name = 'Counter-Strike'
                if game_name == 'League of Legends':
                    game_name = 'LoL'
                bet_total.append(game_name)
                bet_total.append(event['L'].split('.')[1])
                bet_total.append(event['O1'])
                bet_total.append(event['O2'])
                bet_total.append(datetime.fromtimestamp(event['S']).strftime('%d.%m %H:%M'))
                bet_total.append(map)
                if 'Исход' in bet_total_d:
                    bet_total.append(bet_total_d['Исход'])

                bet_total.append(coefs)
                bet_total.append(current_time)

                if len(coefs) > 0:
                    bet_list.append(bet_total)
        # Получение списков с исходами на карты
        if current_id == game_id:
            bet_map_d = {}
            bet_map_d['Название матча'] = event['L']
            bet_map_d['Team 1'] = event['O1']
            bet_map_d['Team 2'] = event['O2']
            bet_map_d['Время'] = event['S']
            try:
                bets = event['SG']
            except KeyError:
                continue
            for item in bets:
                bet = item['PN']
                map = ''
                coefs = []
                for node in item['E']:
                    table_cell = node['T']
                    map = item['PN']
                    bet_map_d['Карта'] = map
                    if 1 == table_cell:
                        coef1 = node['C']
                        coefs.append(coef1)
                    if 3 == table_cell:
                        coef2 = node['C']
                        coefs.append(coef2)
                bet_map = []
                bet_map.append('line')
                bet_map.append('1x')
                game_name = event['L'].split('.')[0]
                if game_name == 'CS 2':
                    game_name = 'Counter-Strike'
                if game_name == 'League of Legends':
                    game_name = 'LoL'
                bet_map.append(game_name)
                bet_map.append(event['L'].split('.')[1])
                bet_map.append(event['O1'])
                bet_map.append(event['O2'])
                bet_map.append(datetime.fromtimestamp(event['S']).strftime('%d.%m %H:%M'))
                bet_map.append(map)
                bet_map.append('Исходы')
                bet_map.append(coefs)
                bet_map.append(current_time)

                if len(coefs) > 0:
                    bet_list.append(bet_map)


    temp_list = []
    for i in bet_list:
        if i not in temp_list:
            temp_list.append((i))
    bet_list = temp_list

    print(*bet_list, sep='\n')
    return bet_list

def get_1x_line_value(event_result):
    session = requests.Session()
    for item in event_result['Value']:
        game_id = item['I']
        champs = item['LI']

        params = {
            'sports': '40',
            'champs': champs,
            'count': '50',
            'tf': '2200000',
            'tz': '3',
            'antisports': '188',
            'mode': '4',
            'subGames': game_id,
            'country': '1',
            'partner': '51',
            'getEmpty': 'true',
            'gr': '44',
        }

        response = session.get('https://1xstavka.ru/LineFeed/Get1x2_VZip', params=params)
        event_result_final = response.json()
        get_final_line(event_result_final, game_id)


def get_1x_line(champ):
    session = requests.Session()
    for i in champ:
        params = {
            'sports': '40',
            'champs': i,
            'count': '50',
            'tf': '2200000',
            'tz': '3',
            'antisports': '188',
            'mode': '4',
            'subGames': '505563290',
            'country': '1',
            'partner': '51',
            'getEmpty': 'true',
            'gr': '44',
        }

        response = session.get('https://1xstavka.ru/LineFeed/Get1x2_VZip', params=params)
        event_result = response.json()

        get_1x_line_value(event_result)


def main():
    session = requests.Session()
    params = {
        'sport': '40',
        'tf': '2200000',
        'tz': '3',
        'country': '1',
        'partner': '51',
        'virtualSports': 'true',
        'gr': '44',
    }

    response = session.get('https://1xstavka.ru/LineFeed/GetChampsZip', params=params)

    champ_id = []
    for ci in response.json()['Value']:
        if 'League of Legends' == ci['SSN'] or 'Dota 2' == ci['SSN'] or 'CS 2' == ci['SSN'] or 'Valorant' == ci['SSN']:
            champ_id.append(ci['LI'])


    get_1x_line(champ_id)




if __name__ == '__main__':
    main()