import grequests
from _datetime import datetime, timedelta
from filtertour import filterteam, filtertourn

bet_list_final = []
def get_coef(game_result):
    global bet_list_final
    global filterteam
    game_name ={'DOTA2': 'Dota 2', 'CS2': 'Counter-Strike', '无畏契约': 'Valorant', '英雄联盟': 'Lol'}
    now = datetime.now()
    current_time = now.strftime('%d.%m.%Y %H:%M')
    for item in game_result:
        kefs = []
        for i in range(len(item['result']['odds'])):
            if item['result']['odds'][i]['group_short_name'] == 'Winner':
                kefs.append(item['result']['odds'][i]['odds'])
                kefs.append(item['result']['odds'][i]['name'])
        if len(kefs) > 0:
            time = datetime.strptime(item['result']['start_time'], "%Y-%m-%d %H:%M:%S") - timedelta(
                hours=5, )
            time = time.strftime('%d.%m.%Y %H:%M')
            if time < current_time:

                time = datetime.strptime(item['result']['start_time'], "%Y-%m-%d %H:%M:%S") - timedelta(
                    hours=5, )
                time = time.strftime('%d.%m.%Y %H:%M')
                if time < current_time:
                    bet_list = []
                    bet_list.append('live')
                    bet_list.append('raybet')
                    game_check = item['result']['game_name']
                    if game_check in game_name:
                        game_check = game_name[game_check]
                    bet_list.append(game_check)
                    bet_list.append(item['result']['tournament_short_name'])
                    team1 = item['result']['team'][0]['team_name'].rstrip().lower().title().replace('Club', '').replace(
                        'Team', '').replace(
                        'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                                   ' ').replace(
                        'Challengers', '').replace('Chall', '').replace('Acad', 'Academy').strip()
                    team2 = item['result']['team'][1]['team_name'].rstrip().lower().title().replace('Club', '').replace(
                        'Team', '').replace(
                        'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                                   ' ').replace(
                        'Challengers', '').replace('Chall', '').replace('Acad', 'Academy').strip()
                    bet_list.append(filterteam.get(team1, team1))
                    bet_list.append(filterteam.get(team2, team2))
                    bet_list.append(time)
                    bet_list_copy = bet_list.copy()
                    if item['result']['round'] == 'bo2':
                        bet_list.append('1-я карта')
                    else:
                        bet_list.append('Общая')
                    bet_list.append('Исходы')
                    if kefs[1].startswith(bet_list[4]):
                        kefs_event = [kefs[0], kefs[2]]
                        bet_list.append(kefs_event)
                    else:
                        kefs_event = [kefs[2], kefs[0]]
                        bet_list.append(kefs_event)
                    bet_list.append(current_time)
                    if len(bet_list) > 0:
                        bet_list_final.append(bet_list)

                    if len(kefs) > 4:
                        bet_list = bet_list_copy.copy()
                        if item['result']['round'] == 'bo2':
                            bet_list.append('2-я карта')
                        else:
                            bet_list.append('1-я карта')

                        bet_list.append('Исходы')
                        if kefs[5].startswith(bet_list[4]):
                            kefs_event = [kefs[4], kefs[6]]
                            bet_list.append(kefs_event)
                        else:
                            kefs_event = [kefs[6], kefs[4]]
                            bet_list.append(kefs_event)

                        bet_list.append(current_time)
                        if len(bet_list) > 0:
                            bet_list_final.append(bet_list)
                    if len(kefs) > 8:
                        bet_list = bet_list_copy.copy()
                        bet_list.append('2-я карта')
                        bet_list.append('Исходы')
                        if kefs[9].startswith(bet_list[4]):
                            kefs_event = [kefs[8], kefs[10]]
                            bet_list.append(kefs_event)
                        else:
                            kefs_event = [kefs[10], kefs[8]]
                            bet_list.append(kefs_event)
                        bet_list.append(current_time)
                        if len(bet_list) > 0:
                         bet_list_final.append(bet_list)
                    kefs = []
                    for i in range(len(item['result']['odds'])):
                        if item['result']['odds'][i]['group_short_name'] == 'Round Handicap':
                            kefs.append(item['result']['odds'][i]['odds'])
                            kefs.append(item['result']['odds'][i]['name'])
                    if len(kefs) > 0:
                        bet_fora = bet_list_copy.copy()
                        bet_fora.append('1-я карта')
                        if kefs[1].startswith(bet_fora[4]):
                            bet_fora.append('Фора 1 (' + str(kefs[1])[-4:] + ')')
                            kefs_fora = [kefs[0], kefs[2]]
                            bet_fora.append(kefs_fora)
                        else:
                            bet_fora.append('Фора 1 ('+ str(kefs[3])[-4:] + ')')
                            kefs_fora = [kefs[2], kefs[0]]
                            bet_fora.append(kefs_fora)
                        bet_fora.append(current_time)
                        if len(bet_fora) > 0:
                            bet_list_final.append(bet_fora)
                    if len(kefs) > 4:
                        bet_fora = bet_list_copy.copy()
                        bet_fora.append('2-я карта')
                        if kefs[5].startswith(bet_fora[4]):
                            bet_fora.append('Фора 1 ('+ str(kefs[5])[-4:] + ')')
                            kefs_fora = [kefs[4], kefs[6]]
                            bet_fora.append(kefs_fora)
                        else:
                            bet_fora.append('Фора 1 (' + str(kefs[7])[-4:] + ')')
                            kefs_fora = [kefs[6], kefs[4]]
                            bet_fora.append(kefs_fora)
                        bet_fora.append(current_time)
                        if len(bet_fora) > 0:
                            bet_list_final.append(bet_fora)
                        kefs = []
                        for i in range(len(item['result']['odds'])):

                            if item['result']['odds'][i]['group_short_name'] == 'Total Rounds' and (item['result']['odds'][i]['value'] != 'odd' or item['result']['odds'][i]['value'] != 'even'):
                                kefs.append(item['result']['odds'][i]['odds'])
                                kefs.append(item['result']['odds'][i]['value'])
                        if len(kefs) > 0:
                            bet_total = bet_list_copy.copy()
                            bet_total.append('1-я карта')
                            total_map = 'Тотал Б (' + str(kefs[1])[1:] +')'
                            bet_total.append(total_map)
                            if kefs[1].startswith('>'):
                                kefs_total = [kefs[0], kefs[2]]
                                bet_total.append(kefs_total)
                            else:
                                kefs_total = [kefs[2], kefs[0]]
                                bet_total.append(kefs_total)
                            bet_total.append(current_time)
                            if len(bet_total) > 0:
                                bet_list_final.append(bet_total)
                        if len(kefs) > 4:
                            bet_total = bet_list_copy.copy()
                            bet_total.append('2-я карта')
                            total_map = 'Тотал Б (' + str(kefs[1])[1:] +')'
                            bet_total.append(total_map)
                            if kefs[5].startswith('>'):
                                kefs_total = [kefs[4], kefs[6]]
                                bet_total.append(kefs_total)
                            else:
                                kefs_total = [kefs[6], kefs[4]]
                                bet_total.append(kefs_total)
                            bet_total.append(current_time)
                            if len(bet_total) > 0:
                                bet_list_final.append(bet_total)
    return(bet_list_final)

def get_game_result(bet_id):
    game_result = []
    requests = []
    for id in bet_id:
        params = {'match_id': id}
        request = grequests.get('https://vnimpvgameinfo.esportsworldlink.com/v2/odds', params=params)
        requests.append(request)
    responses = grequests.map(requests)
    for response in responses:
        if response is not None:
            game_result.append(response.json())
    bet_list_final = get_coef(game_result)
    return bet_list_final

def get_id(result_list):
    bet_id = []
    for result in result_list:
        for event in result['result']:

            if event['game_name'] == 'CS2' or event['game_name'] == '无畏契约' or event['game_name'] == '英雄联盟' or event[
                'game_name'] == 'DOTA2':  # 2 val  4 lol
                bet_id.append(event['id'])
    bet_list_final = get_game_result(bet_id)
    return bet_list_final

def raybetlive():
    result_list = []
    match_type = 1
    requests = []
    for page in range(1, 3):
        params = {'page': page,'match_type': match_type}
        request = grequests.get('https://vnimpvgameinfo.esportsworldlink.com/v2/match', params=params)
        requests.append(request)
    responses = grequests.map(requests)
    for response in responses:
        if response is not None:
            result_list.append(response.json())
    return get_id(result_list)


if __name__ == '__main__':
    print(*raybetlive(), sep='\n')