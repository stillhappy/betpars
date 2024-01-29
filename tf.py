import requests

# линия
def get_matches_line():
    url = "https://api-v4.ely889.com/api/v4/events/paginate"

    querystring = {"combo": "false", "outright": "false", "timing": "today", "sort_by_popular": "true",
                   "market_option": "MATCH", "lang": "en", "timezone": "Europe^%^2FMoscow"}

    payload = ""
    headers = {
        "authority": "api-v4.ely889.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Token 9278cadf62902610a21cfecfc60b8eeb2c830e93",
        "origin": "https://gc.ely889.com",
        "public-token": "b8c712a2f691483381abad76cef9f67d",
        "referer": "https://gc.ely889.com/",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tf-authorization": "86013c6bcc22c686fab14f2e7c4643b64b1d854fc885031dc7613be767cfaa0324fd21364f15aec6b60e54dcc89416b59217c819e9e27024f8adf43c74caa079",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response.json()['results']

print(get_matches_line())

