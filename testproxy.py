from random import choice
import requests
import lxml
from fake_useragent import UserAgent
# Указываем URL, к которому будем отправлять запрос для тестирования прокси
url = 'https://www.fon.bet/sports/esports/'
ua = UserAgent()
# Открываем файл с прокси и читаем его
with open('proxy.txt') as file:
    # Считываем содержимое файла и разделяем его на строки
    proxy_file = file.read().split('\n')
    n = 1
    for _ in range(10):
        try:

            print(f'попытка номер:{n}')
            n += 1
            # Выбираем случайный прокси из списка и удаляем лишние пробелы
            ip = choice(proxy_file).strip()
            fake_ua = {'user-agent': ua.random}
            print(ip)

            # Формируем словарь с прокси для http и https
            proxy = {
                'https': f'http://{ip}'
            }
            # Выполняем GET-запрос с использованием выбранного прокси
            response = requests.get(url=url, proxies=proxy, headers=fake_ua)
            print(response.status_code)
            # Выводим результат в случае успешного подключения
            print(response.json(), 'Success connection')
        except Exception as _ex:
            # В случае неудачи пропускаем текущую итерацию
            continue