import time
from bs4 import BeautifulSoup
import requests


def get_urls(soup):
    urls = soup.findAll('a', class_='search_result_row')
    urlsRes = []
    for data in urls:
        urlsRes.append(data['href'])

    return urlsRes


def get_popularity(soup) -> int:
    popularity = soup.findAll('span', class_='responsive_hidden')
    filteredPopularity = []

    for data in popularity:
        filteredPopularity.append(*data.text.split())

    filteredPopularity[1] = filteredPopularity[1].replace(',', '')
    filteredPopularity[1] = filteredPopularity[1].replace('(', '')
    filteredPopularity[1] = filteredPopularity[1].replace(')', '')

    return int(filteredPopularity[1])


def get_tags(soup) -> list:

    allTags = soup.findAll('a', class_='app_tag')
    filteredTags = []
    for data in allTags:
        filteredTags.append(data.text.split())

    return filteredTags


main_url = 'https://store.steampowered.com/search/'
main_page = requests.get(main_url)
main_soup = BeautifulSoup(main_page.text, "html.parser")
urls = get_urls(main_soup)


for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    tag = get_tags(soup)
    popularity = get_popularity(soup)
    print(*tag, '\n', popularity)

    time.sleep(10)
