import re
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
    soup = BeautifulSoup(content, 'html.parser')
    dirty_price = soup.find('span', 'as-price-currentprice').text
    price = float(dirty_price.strip().strip('$'))
    status = 'SUCCESS' if price else 'FAIL'
    sale_price = 0
    if soup.find(string=re.compile('sale price')):
        sale_price = soup.find(string=re.compile('sale price'))

    return {
        'price': price,
        'status': status,
        'sale_price': sale_price,
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
