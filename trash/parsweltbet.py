from bs4 import BeautifulSoup as bs
import lxml
from datetime import datetime, timedelta
import requests
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# функция для сбора ссылок на все нужные матчи
def get_links(driver):
    driver.get('https://weltbet11.com/ru/esports')
    time.sleep(1)
    matches = driver.find_elements(By.CLASS_NAME, 'league-item')
    links = []
    valid_games = {'CS2', 'Dota 2'}
    for match in matches:
        match.click()
        game = match.find_element(By.CLASS_NAME, 'league-title-label.text-truncate').text
        if game.split(' - ')[0] not in valid_games:
            continue
        links_full = match.find_elements(By.TAG_NAME, 'a')
        for link in links_full:
            links.append(link.get_attribute('href'))
    return links


async def get_html_code(driver, url):
    await asyncio.gather(
        driver.get(url),
        driver.page_source()
    )
    html_code = await driver.page_source
    return html_code


async def main():
    proxy = '45.145.160.130:8000'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    links = get_links(driver)
    print(len(links))
    tasks = []
    for url in links:
        task = asyncio.ensure_future(get_html_code(driver, url))
        tasks.append(task)

    html_codes = await asyncio.gather(*tasks)

    # Дальнейшие операции с полученными HTML-кодами
    for html_code in html_codes:
        print(html_code[:10])
        # Выполнение дополнительных операций с HTML-кодом

    # Закрытие драйвера
    driver.quit()


if __name__ == '__main__':
    asyncio.run(main())