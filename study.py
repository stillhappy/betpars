import requests
import lxml
from bs4 import BeautifulSoup as bs
summ = 0
lst = ['watch', 'mobile', 'mouse', 'hdd', 'headphones']
for i, key in enumerate(lst):
    for j in range(32):
        url = f'https://parsinger.ru/html/{key}/{i+1}/{i+1}_{j+1}.html'
        response = requests.get(url=url)
        response.encoding='utf-8'
        soup = bs(response.text, 'lxml')
        n = int(soup.find('span', id='in_stock').text.replace('В наличии: ',''))
        price = int(soup.find('span', id='price').text.replace(' руб',''))
        summ += n*price
print(summ)

