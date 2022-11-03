import time
from bs4 import BeautifulSoup
import requests



def get_urls(soup) -> list:

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

    all_tags = soup.findAll('a', class_='app_tag')
    filtered_tags = []
    for data in all_tags:
        filtered_tags.append(data.text.strip())

    return filtered_tags


def get_game_name(soup) -> str:

    all_names = soup.findAll('div', class_="apphub_AppName")
    filtered_names = []
    for name in all_names:
        filtered_names.append(name.text)

    return filtered_names[0]

main_url = 'https://store.steampowered.com/search/'
main_page = requests.get(main_url)
main_soup = BeautifulSoup(main_page.text, "html.parser")
urls = get_urls(main_soup)


for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    tags = get_tags(soup)
    popularity = get_popularity(soup)
    name = get_game_name(soup)
    print("Тэги:\n", *tags, '\nПопулярность:\n', popularity, '\nИмя:', name)

    time.sleep(45)

