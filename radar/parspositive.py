import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import lxml
from datetime import datetime as dt
import requests
import itertools
from fake_useragent import UserAgent
from random import choice


prox = ['http://45.143.167.92:8000', 'http://138.124.186.18:8000', 'http://193.9.17.244:8000']

url = "https://csgopositive.me/lib/bets.php"
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

def get_line_live_pos2(line_live):
    response = requests.get('https://csgopositive.me/')
    response.encoding = 'utf-8'
    bdposid = []
    filterposbk = {'valorant': 'Valorant', 'lol': 'LoL', 'csgo': 'Counter-Strike', 'dota2': 'Dota 2'}
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
            if game[-1] in ['live_betting', 'live_betting_upcoming']:
                gamex = game[-2].split('_')[0]
            else:
                gamex = game[-1].split('_')[0]
            if gamex not in filterposbk:
                continue
            bdpos2.append(filterposbk[gamex])
            bdpos2.append(ci.find('span', class_='event_name').text)
            if ci.find('span', class_='event_name').text in ['CS2 Positive duo aim ', 'CS2 Positive aim ', 'CS2 Positive duo aim', 'CS2 Positive aim']:
                continue
            bdpos2.append(ci.find_all('span', class_='team_name')[0].text.rstrip().lower().title().replace('Club', '').replace('Team', '').replace('Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ', ' ').strip())
            bdpos2.append(ci.find_all('span', class_='team_name')[1].text.rstrip().lower().title().replace('Club', '').replace('Team', '').replace('Esports', '').replace('Esport', '').replace('E-Sports', '').replace('Gaming', '').replace('  ', ' ').strip())
            data_match = dt.strptime(ci.find(class_='timer').get('data-start'), '%m/%d/%Y %H:%M:%S').strftime(
                '%Y-%m-%d %H:%M')
            bdpos2.append(data_match)
            bdpos2.append([f"action=get_koef&event_id={ci.get('data-id')}&team_id=1&lang=RU", f"action=get_koef&event_id={ci.get('data-id')}&team_id=2&lang=RU"])
            bdposid.append(bdpos2)
    return bdposid

def get_line_live_pos22(lst):
    now = dt.now()
    current_time = now.strftime('%Y-%m-%d %H:%M')
    bdpos = []
    dct = {'Победа в матче': 'Общая', 'Победа в серии BO3': 'Общая', 'Победа на карте #1': '1-я карта',
           'Победа на карте #2': '2-я карта', 'Победа на карте #3': '3-я карта', 'Победа на карте #4': '4-я карта',
           'Победа на карте #5': '5-я карта'}

    dct2 = {'Исходы': ['Победа в серии BO3', 'Победа на карте #1', 'Победа на карте #2', 'Победа на карте #3',
                       'Победа на карте #4', 'Победа на карте #5', 'Победа в матче'],
            'Сделают первое убийство': 'Первая кровь',
            'Сделают первыми 5 убийств': 'Гонка до 5 киллов', 'Сделают первыми 10 убийств': 'Гонка до 10 киллов',
            'больше 21.5': 'Тотал Б (21.5)', 'меньше 21.5': 'Тотал Б (21.5)', 'больше 20.5': 'Тотал Б (20.5)',
            'меньше 20.5': 'Тотал Б (20.5)'}

    for k in lst:
        a1, b1 = k[8][0], k[8][1]
        if not a1:
            continue
        x = a1[0].previous_sibling.text.strip()
        if x not in dct:
            continue
        for ci, cj in zip(a1, b1):
            bdpos1 = k[:7].copy()
            if ci.previous_sibling.text.strip() != x and ci.previous_sibling.text.strip() in dct:
                x = ci.previous_sibling.text.strip()

            if ci.previous_sibling.text.strip() == x:
                bdpos1.append(dct[ci.previous_sibling.text.strip()])
                bdpos1.append('Исходы')
                bdpos1.append([ci.text, cj.text])
                bdpos1.append(current_time)
            if ci.previous_sibling.text.strip() != x and ci.previous_sibling.text.strip() not in dct and ci.previous_sibling.text.strip() in dct2:
                if ci.previous_sibling.text.strip() in ['больше 21.5', 'больше 20.5']:
                    bdpos1.append(dct[x])
                    bdpos1.append(dct2[ci.previous_sibling.text.strip()])
                    bdpos1.append([ci.text])

                elif ci.previous_sibling.text.strip() in ['меньше 21.5', 'меньше 20.5']:
                    bdpos[-1][-1].append(cj.text)
                    bdpos[-1].append(current_time)
                    continue
                else:
                    bdpos1.append(dct[x])
                    bdpos1.append(dct2[ci.previous_sibling.text.strip()])
                    bdpos1.append([ci.text, cj.text])
                    bdpos1.append(current_time)
            if len(bdpos1) > 7:
                bdpos.append(bdpos1)
    return bdpos

async def get_url(payload):
    global url, headers, prox
    ua = UserAgent(min_percentage=1.5)
    proxi = choice(prox)
    headers["user-agent"] = ua.random
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload[7][0], headers=headers, proxy=proxi) as resp:
            if resp.status == 429:
                await asyncio.sleep(1)
            soup = bs(await resp.text(), 'lxml')
            a = soup.find_all(class_='koef')
        async with session.post(url, data=payload[7][1], headers=headers, proxy=proxi) as resp:
            if resp.status == 429:
                await asyncio.sleep(1)
            soup = bs(await resp.text(), 'lxml')
            b = soup.find_all(class_='koef')
    payload.append([a, b])
    return [payload]

async def positive():
    tasks = [get_url(payload) for payload in get_line_live_pos2('line') + get_line_live_pos2('live')]
    try:
        results = await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Корутины были отменены до завершения")
        return
    combined_list = list(itertools.chain.from_iterable(results))
    line_pos = get_line_live_pos22(combined_list)
    print(*line_pos, sep='\n')

if __name__ == '__main__':
    asyncio.run(positive())