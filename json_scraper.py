import json
import requests
from selenium import webdriver

from bs4 import BeautifulSoup

TARGET_URL = 'https://www.apple.com/shop/buy-iphone/iphone-7/\
4.7-inch-display-32gb-black-unlocked#00,20,31,40,60'


def get_http_response_by_selenium(url: str) -> str:
    driver = webdriver.Firefox()
    driver.get(url)
    raw_html = driver.execute_script(
                    "return document.documentElement.outerHTML")
    driver.close()
    return raw_html


def get_http_response(url: str) -> str:
    return requests.get(url).content


def fetch_response(content: str) -> dict:
    attributes = {'type': 'application/ld+json'}
    sale_keys = ['sale', 'sale_price', 'sale price']
    search_key = 'offers'
    _data = None

    soup = BeautifulSoup(content, 'html.parser')
    scripts_soup = soup.find('head').find_all('script', attrs=attributes)
    for script in scripts_soup:
        if search_key in script.text:
            _data = json.loads(script.text)[search_key][0]
            break

    price = float(_data['price']) if 'price' in _data.keys() else 0
    status = 'SUCCESS' if price else 'FAIL'
    sale_price = 0
    for k in sale_keys:
        if k in _data.keys():
            sale_price = int(_data[k])

    return {
        'price': price,
        'status': status,
        'sale_price': sale_price
    }


def scrape_price_data(url: str, is_selenium=False) -> dict:
    if is_selenium:
        response = get_http_response_by_selenium(url)
    else:
        response = get_http_response(url)
    clean_data = fetch_response(response)
    return clean_data


if __name__ == '__main__':

    print(scrape_price_data(TARGET_URL))
    print(scrape_price_data(TARGET_URL, is_selenium=True))
