from gamesdb import DataBase
from gamesdb import Game, Tag, User


import random


class Guesser:
    def __init__(self):
        self.db = DataBase()

    def close(self):
        self.db.disconnect()

    def guess_game(self, user: User, selection_size=-1) -> list[Game]:
        ans = self.selection(user)
        while len(ans) < selection_size:
            user.delete_useless_tag()
            ans = self.selection(user)

        if selection_size == -1:
            selection_size = len(ans)

        ans = sorted(list(ans), reverse=True)
        return ans[0:selection_size]

    def selection(self, user: User):
        good_games = self.select_good_games(user.good_tags)
        bad_games = self.select_bad_games(user.bad_tags)
        return good_games - bad_games

    def select_good_games(self, tags: list[Tag]) -> set[Game]:
        ans = set(self.db.all_games)
        for tag in tags:
            temp = self.db.get_games_with_tag(tag)
            ans = set(temp) & ans
            if not ans:
                break

        return ans

    def select_bad_games(self, tags: list[Tag]) -> set[Game]:
        ans = set()
        for tag in tags:
            temp = self.db.get_games_with_tag(tag)
            ans = set(temp) | ans

        return ans

    def get_new_tag(self, user: User) -> Tag:
        remaining_tags = self.db.get_possible_tags(user)
        remaining_tags.sort()

        weights = [tag.usage_count for tag in remaining_tags]
        return random.choices(remaining_tags, weights=weights)[0]
