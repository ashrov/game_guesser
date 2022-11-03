import time
from bs4 import BeautifulSoup
import requests


def get_urls(soup):
    urls = soup.findAll('a', class_='search_result_row')
    urlsRes = []
    for data in urls:
        urlsRes.append(data['href'])

    print(urlsRes)


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

# file = open('games.txt', encoding="utf8")
# game_ids = []
# for string in file:
#     print(string[0])
#

game_id = 730
url = f'https://store.steampowered.com/app/{game_id}/'
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

main_url = 'https://store.steampowered.com/search/'
main_page = requests.get(main_url)
main_soup = BeautifulSoup(main_page.text, "html.parser")

get_urls(main_soup)
