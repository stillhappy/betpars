import requests

url = "https://line07w.bk6bba-resources.com/line/mobile/showSports"

querystring = {"sysId":"2","lang":"ru","lineType":"full_line","skId":"29086","scopeMarket":"1600"}

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
    "sec-ch-ua": "^\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

idtor = response.json()['sports']
ids = [ci['id'] for ci in idtor]

print(ids)