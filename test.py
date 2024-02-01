import requests
from bs4 import BeautifulSoup as bs
import lxml

def get_match_pos(event_id):
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
    response1 = requests.request("POST", url, data=payload1, headers=headers)
    response2 = requests.request("POST", url, data=payload2, headers=headers)
    soup1 = bs(response1.text, 'lxml')
    soup2 = bs(response2.text, 'lxml')
    return soup1, soup2

dct = {'Победа в матче': 'Общая', 'Победа в серии BO3': 'Общая', 'Победа на карте #1': '1-я карта', 'Победа на карте #2': '2-я карта', 'Победа на карте #3': '3-я карта', 'Победа на карте #4': '4-я карта', 'Победа на карте #5': '5-я карта'}
dct2 = {'Исходы': ['Победа в серии BO3', 'Победа на карте #1', 'Победа на карте #2', 'Победа на карте #3', 'Победа на карте #4', 'Победа на карте #5', 'Победа в матче'], 'Сделают первое убийство': 'Первая кровь',
       'Сделают первыми 5 убийств':'Гонка до 5 киллов', 'Сделают первыми 10 убийств': 'Гонка до 10 киллов', 'больше 21.5': 'Тотал Б (21.5)', 'меньше 21.5': 'Тотал Б (21.5)', 'больше 20.5': 'Тотал Б (20.5)', 'меньше 20.5': 'Тотал Б (20.5)'}
# 165325 cs
# 165466 dota
# 165195 lol
# 165027 valik
bdpos1 = []
for k in [165256]:
    a, b = get_match_pos(k)
    a1 = a.find_all(class_='koef')
    b1 = b.find_all(class_='koef')
    bdpos2 = [k]
    x = a1[0].previous_sibling.text.strip()
    for ci, cj in zip(a1, b1):
        bdpos3 = bdpos2.copy()
        if ci.previous_sibling.text.strip() != x and ci.previous_sibling.text.strip() in dct:
            x = ci.previous_sibling.text.strip()

        if ci.previous_sibling.text.strip() == x:
            bdpos3.append(dct[ci.previous_sibling.text.strip()])
            bdpos3.append('Исходы')
            bdpos3.append([ci.text, cj.text])
        if ci.previous_sibling.text.strip() != x and ci.previous_sibling.text.strip() not in dct and ci.previous_sibling.text.strip() in dct2:
            if ci.previous_sibling.text.strip() in ['больше 21.5', 'больше 20.5']:
                bdpos3.append(dct[x])
                bdpos3.append(dct2[ci.previous_sibling.text.strip()])
                bdpos3.append([ci.text])
            elif ci.previous_sibling.text.strip() in ['меньше 21.5', 'меньше 20.5']:
                bdpos1[-1][-1].append(cj.text)
                continue
            else:
                bdpos3.append(dct[x])
                bdpos3.append(dct2[ci.previous_sibling.text.strip()])
                bdpos3.append([ci.text, cj.text])


        if len(bdpos3)>1:
            bdpos1.append(bdpos3)



print(*bdpos1,sep='\n')
