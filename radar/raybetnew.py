from datetime import datetime
from datetime import timedelta
import asyncio
import aiohttp
import itertools
import json
from filtertour import filterteam, filtertourn
from random import choice


def norm_imena(team1, team2):
    team1 = team1.rstrip().lower().title().replace('Club', '').replace(
            'Team', '').replace(
            'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                       ' ').replace(
            'Challengers', '').replace('Chall', '').strip()
    team2 = team2.rstrip().lower().title().replace('Club', '').replace(
            'Team', '').replace(
            'Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ',
                                                                                                       ' ').replace(
            'Challengers', '').replace('Chall', '').strip()
    return (team1, team2)
def get_coef(game_result):
    bet_list_final = []
    game_name = {'DOTA2': 'Dota 2', 'CS2': 'Counter-Strike', '无畏契约': 'Valorant', '英雄联盟': 'LoL'}
    param_name = {'final': 'Общая', 'r1': '1-я карта', 'r2': '2-я карта', 'r3': '3-я карта', 'r4': '4-я карта', 'r5': '5-я карта',
                  'map1': '1-я карта', 'map2': '2-я карта', 'map3': '3-я карта', 'map4': '4-я карта', 'map5': '5-я карта'}
    bet_names = {'Winner': 'Исходы', 'Draw First Blood': 'Первая кровь', '1st Pistol Round - Winner': '1-й Пистолетный раунд',
                 '2st Pistol Round - Winner': '2-й Пистолетный раунд', '5 Kills': 'Гонка до 5 киллов',
                 '10 Kills': 'Гонка до 10 киллов', '15 Kills': 'Гонка до 15 киллов'}
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    date_format = '%Y-%m-%d %H:%M'
    initial_date = datetime.strptime(current_time, date_format)
    updated_date = initial_date + timedelta(hours=3)
    current_time = updated_date.strftime(date_format)
    for game in game_result:
        res = game['result']
        bet_list = ['line' if res['status'] == 1 else 'live', 'raybet']
        if res['game_name'] in game_name:
            bet_list.append(game_name[res['game_name']])
        else:
            continue
        bet_list.append(res['tournament_short_name'])
        bet_list.extend([res['team'][0]['team_name'], res['team'][1]['team_name']])
        time = res['start_time']
        date_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        new_date_obj = date_obj - timedelta(hours=5)
        new_date_string = new_date_obj.strftime("%Y-%m-%d %H:%M:%S")
        bet_list.append(new_date_string)
        last_bet = ''
        for i in range (len(res['odds'])):
            odd = res['odds'][i]
            name_bet = odd['group_short_name']
            name_param = odd['match_stage']
            if name_bet in ['Winner', 'Draw First Blood', '1st Pistol Round - Winner', '2st Pistol Round - Winner', '5 Kills', '10 Kills', '15 Kills'] and odd['tag'] == 'win':
                if not last_bet:
                    last_bet = name_bet
                    cofs = odd['odds']
                else:
                    bet_list_1 = bet_list.copy()
                    bet_list_1.append(param_name[odd['match_stage']])
                    bet_list_1.append(bet_names[name_bet])
                    if odd['name'] == bet_list[5]:
                        bet_list_1.append([cofs, odd['odds']])
                    else:
                        bet_list_1.append([odd['odds'], cofs])
                    bet_list_1.append(current_time)
                    last_bet = ''
                    team1, team2 = norm_imena(bet_list_1[4], bet_list_1[5])
                    bet_list_1[4], bet_list_1[5] = filterteam.get(team1, team1), filterteam.get(team2, team2)
                    bet_list_final.append(bet_list_1)
            elif name_bet == 'Round Handicap':
                if not last_bet:
                    last_bet = odd['value']
                    cofs = odd['odds']
                else:
                    bet_list_1 = bet_list.copy()
                    bet_list_1.append(param_name[odd['match_stage']])
                    if odd['name'][:-6] == bet_list[5]:
                        bet_list_1.append(f"Фора 1 ({last_bet})")
                        bet_list_1.append([cofs, odd['odds']])
                    else:
                        bet_list_1.append(f"Фора 1 ({odd['value']})")
                        bet_list_1.append([odd['odds'], cofs])
                    bet_list_1.append(current_time)
                    last_bet = ''
                    team1, team2 = norm_imena(bet_list_1[4], bet_list_1[5])
                    bet_list_1[4], bet_list_1[5] = filterteam.get(team1, team1), filterteam.get(team2, team2)
                    bet_list_final.append(bet_list_1)
            elif name_bet == 'Total Rounds':
                if not last_bet:
                    last_bet = odd['value']
                    cofs = odd['odds']
                else:
                    bet_list_1 = bet_list.copy()
                    bet_list_1.append(param_name[odd['match_stage']])
                    if '>' in last_bet:
                        bet_list_1.append(f"Тотал Б ({last_bet[1:]})")
                        bet_list_1.append([cofs, odd['odds']])
                    else:
                        bet_list_1.append(f"Тотал Б ({odd['value'][1:]})")
                        bet_list_1.append([odd['odds'], cofs])
                    bet_list_1.append(current_time)
                    last_bet = ''
                    team1, team2 = norm_imena(bet_list_1[4], bet_list_1[5])
                    bet_list_1[4], bet_list_1[5] = filterteam.get(team1, team1), filterteam.get(team2, team2)
                    bet_list_final.append(bet_list_1)
            elif name_bet == 'Total Kills Odd/Even' and bet_list[2] == 'Dota 2' or name_bet == 'Total Rounds Odd/Even' and bet_list[2] == 'Counter-Strike':
                if not last_bet:
                    last_bet = odd['value']
                    cofs = odd['odds']
                else:
                    bet_list_1 = bet_list.copy()
                    bet_list_1.append(param_name[odd['match_stage']])
                    bet_list_1.append(f"Тотал {'Киллов' if bet_list[2] == 'Dota 2' else 'Раундов'} (Odd/Even)")
                    if 'odd' in last_bet:
                        bet_list_1.append([cofs, odd['odds']])
                    else:
                        bet_list_1.append([odd['odds'], cofs])
                    bet_list_1.append(current_time)
                    last_bet = ''
                    team1, team2 = norm_imena(bet_list_1[4], bet_list_1[5])
                    bet_list_1[4], bet_list_1[5] = filterteam.get(team1, team1), filterteam.get(team2, team2)
                    bet_list_final.append(bet_list_1)


                # print(odd['tag'], odd['name'], odd['odds'], odd['value'], odd['group_short_name'], odd['match_stage'])
    return bet_list_final


        # final - общая, r1-5 - карты1-5 or map1-5
        # Мне надо Winner, Match Handicap, Total Maps, Draw First Blood, 5/10/15 kills, Total kills Odd/Even |||| DOTA
        # Мне надо Winner, Match Handicap, Total Maps, Total Rounds, Total kills Odd/Even, 1-2st Pistol Round - Winner, Round Handicap |||| CS

async def get_urls(page):
    querystring = {"page": page[0], "match_type": page[1]}
    proxi = choice(['http://45.145.160.130:8000', 'http://138.124.186.18:8000', 'http://193.9.17.244:8000'])
    url = "https://vnimpvgameinfo.esportsworldlink.com/v2/match"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=querystring, proxy=proxi) as resp:
                if resp.status == 200:
                    resjs = await resp.json()
                    matches_id = [res['id'] for res in resjs['result'] if res['game_id'] in [151, 140, 70, 37197927]]
                else:
                    matches_id = []  # Пропустить обработку, если возникла ошибка
        except Exception as e:
            print(f"Произошла ошибка при получении данных: {e}")
            matches_id = []  # Пропустить обработку, если возникла ошибка
    return matches_id

async def get_json_matches(match_id):
    proxi = choice(['http://45.145.160.130:8000', 'http://138.124.186.18:8000', 'http://193.9.17.244:8000'])
    querystring = {"match_id": match_id}
    url = "https://vnimpvgameinfo.esportsworldlink.com/v2/odds"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=querystring, proxy=proxi) as resp:
            if resp.content_type != 'application/json':
                return []
            else:
                match_json = await resp.json()
    return [match_json]

async def raybet():
    pages = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (1, 1), (2, 1), (1, 0), (2, 0), (3, 0), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
             (7, 3), (8, 3)]
    tasks = [get_urls(page) for page in pages]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    matches_id = list(itertools.chain.from_iterable(results))
    tasks = [get_json_matches(match_id) for match_id in matches_id]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    matches_jsons = list(itertools.chain.from_iterable(results))
    return get_coef(matches_jsons)

if __name__ == '__main__':
    print(*asyncio.run(raybet()), sep='\n')
