from bs4 import BeautifulSoup
import requests
import lxml
response = requests.get('https://csgopositive.me/')
response.encoding = 'utf-8'
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    left_element = soup.select('#upcoming .event .left .team_name')
    right_element = soup.select('#upcoming .event .right .team_name')
    left_cof = soup.select('#upcoming .event .left .sum.odds_icon')
    right_cof = soup.select('#upcoming .event .right .sum.odds_icon')
    event_name = soup.select('#upcoming .event .center .event_name')
    for a,b,c,d,e in zip(left_element,left_cof,right_cof,right_element, event_name):
        print(f'Турнир: {e.text}\n{a.text.lstrip()} ({b.text} - {c.text}) {d.text.lstrip()}')


else:
    print('нельзя',response.status_code)