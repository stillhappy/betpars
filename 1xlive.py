import requests
from _datetime import datetime


bet_list_final = []
def get_final_live(event_result_final):
    global bet_list_final
    game_name = {'CS 2': 'Counter-Strike','League of Legends': 'Lol'}
    now = datetime.now()
    current_time = now.strftime('%d.%m.%Y %H:%M')

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
                bet_list.append(i['O1'])
                bet_list.append(i['O2'])
                bet_list.append(datetime.fromtimestamp(i['S']).strftime('%d.%m.%Y %H:%M'))
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
                    bet_fora.append('Фора 1 (' + str(kef[1]) + ')')
                    bet_fora.append(kef_fora)
                    bet_fora.append(current_time)
                    if len(bet_fora[9]) > 1:
                        bet_list_final.append(bet_fora)
                if len(kef) > 3:
                    bet_fora = bet_list_copy.copy()
                    kef_fora = [kef[3],kef[5]]
                    bet_fora.append('2-я карта')
                    bet_fora.append('Фора 1 (' + str(kef[4]) + ')')
                    bet_fora.append(kef_fora)
                    bet_fora.append(current_time)
                    if len(bet_fora[9]) > 1:
                        bet_list_final.append(bet_fora)
                if len(kef) > 6:
                    bet_fora = bet_list_copy.copy()
                    kef_fora = [kef[6],kef[8]]
                    bet_fora.append('3-я карта')
                    bet_fora.append('Фора 1 (' + str(kef[7]) + ')')
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

def get_1x_live_value(event_result):
    event_result_final = []

    for event in event_result:
        for item in event['Value']:
            champs = (item['LI'])
            game_id =(item['I'])
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

            response = requests.get('https://1xstavka.ru/LiveFeed/Get1x2_VZip', params=params)
            event_result_final.append(response.json())
    bet_list_final = get_final_live(event_result_final)
    return bet_list_final

def get_1x_live(champ):
    event_result = []
    for i in champ:
        params = {
            'sports': '40',
            'champs': i,
            'count': '50',
            'gr': '44',
            'antisports': '188',
            'mode': '4',
            'subGames': '506672024',
            'country': '1',
            'partner': '51',
            'getEmpty': 'true',
        }

        response = requests.get('https://1xstavka.ru/LiveFeed/Get1x2_VZip', params=params)
        event_result.append(response.json())


    bet_list_final = get_1x_live_value(event_result)
    return bet_list_final

def main():
    params = {
        'sport': '40',
        'gr': '44',
        'country': '1',
        'partner': '51',
        'virtualSports': 'true',
    }

    response = requests.get('https://1xstavka.ru/LiveFeed/GetChampsZip', params=params)

    champ_id = []
    for ci in response.json()['Value']:
        if 'League of Legends' == ci['SSN'] or 'Dota 2' == ci['SSN'] or 'CS 2' == ci['SSN'] or 'Valorant' == ci['SSN']:
            champ_id.append(ci['LI'])

    bet_list_final = get_1x_live(champ_id)

    print(*bet_list_final,sep = '\n')




if __name__ == '__main__':
    main()