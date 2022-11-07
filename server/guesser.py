import sqlite3

from database import DataBase
from utils import Game, Tag

db = DataBase()
all_tags = db.get_all_tags()

sqlite_connection = sqlite3.connect('database.db')
cursor = sqlite_connection.cursor()


def search_games(tmp_game: Game) -> list[Game]:
    pass


def get_tag(tmp_game: Game) -> Tag:
    return Tag("", "")


def close():
    db.disconnect()


def guesser(string):
    tags = string.split('_')
    tags.sort(key=compare_tags, reverse=True)
    print(tags)

    for i in range(len(tags)):
        tags[i] = compare_tags(tags[i], 0)

    close()
    return selection(tags)


def selection(tags):
    ans = sort_games(tags)
    flag = False

    while not flag:
        try:
            game_select = "SELECT * from games WHERE id = ?"
            cursor.execute(game_select, (ans[0],))
            record = cursor.fetchall()
            flag = True
        except:
            del (tags[-1])
            ans = sort_games(tags)

    return record


def compare_games(a, num=3):
    rate_select = "SELECT * from games WHERE id = ?"
    cursor.execute(rate_select, (a,))
    record = cursor.fetchone()[num]

    return int(record)


def compare_tags(a, num=3):
    rate_select = "SELECT * from tags WHERE tag_name = ?"
    cursor.execute(rate_select, (a,))
    record = cursor.fetchone()[num]

    return int(record)


def search_one_tag(tags, num):
    game_select = "SELECT * from game_to_tag WHERE tag_id = ?"
    cursor.execute(game_select, (tags[num],))
    games = cursor.fetchall()
    for i in range(len(games)):
        games[i] = games[i][0]
    return games


def sort_games(tags):
    ans = search_one_tag(tags, 0)
    for i in range(1, len(tags)):
        temp = search_one_tag(tags, i)
        ans = list(set(temp) & set(ans))

    ans.sort(key=compare_games, reverse=True)

    return ans
